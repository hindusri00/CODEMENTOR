"""Static analysis: parse Java into an AST and collect *facts* about the code.

These facts are given to the LLM as grounded evidence, so it doesn't have to
guess (e.g. "there are 2 nested loops at line 5"). This reduces hallucination.
"""
from dataclasses import dataclass, field
import javalang
from javalang import tree as T

LOOP_TYPES = (T.ForStatement, T.WhileStatement, T.DoStatement)


@dataclass
class Finding:
    kind: str
    line: int | None
    detail: str


@dataclass
class StaticReport:
    parsed: bool = True
    parse_error: str = ""
    max_loop_depth: int = 0
    findings: list[Finding] = field(default_factory=list)

    @property
    def heuristic_complexity(self) -> str:
        d = self.max_loop_depth
        if d == 0:
            return "O(1) or O(n) via library calls (no explicit loops)"
        return "O(n)" if d == 1 else f"O(n^{d}) (heuristic: based on loop nesting)"

    def to_text(self) -> str:
        if not self.parsed:
            return f"(Could not parse code: {self.parse_error})"
        lines = [
            f"Max loop nesting depth: {self.max_loop_depth}",
            f"Heuristic time complexity: {self.heuristic_complexity}",
        ]
        for f in self.findings:
            loc = f"line {f.line}" if f.line else "unknown line"
            lines.append(f"- [{f.kind}] {loc}: {f.detail}")
        return "\n".join(lines)


def _parse(code: str):
    """Try the code as-is, then wrapped as a class body, then as a method body.
    Returns (ast, line_offset)."""
    attempts = [
        (code, 0),
        ("class Wrapper {\n" + code + "\n}", 1),
        ("class Wrapper { void run() {\n" + code + "\n} }", 1),
    ]
    last_err = None
    for src, offset in attempts:
        try:
            return javalang.parse.parse(src), offset
        except Exception as e:  # javalang raises several exception types
            last_err = e
    raise ValueError(str(last_err))


def _walk(node, depth, visit):
    if isinstance(node, T.Node):
        d = depth + 1 if isinstance(node, LOOP_TYPES) else depth
        visit(node, d)
        for child in node.children:
            _walk(child, d, visit)
    elif isinstance(node, (list, tuple, set)):
        for c in node:
            _walk(c, depth, visit)


def analyze(code: str) -> StaticReport:
    report = StaticReport()
    try:
        ast, off = _parse(code)
    except ValueError as e:
        report.parsed = False
        report.parse_error = str(e)
        return report

    def line_of(node):
        pos = getattr(node, "position", None)
        line = getattr(pos, "line", None)
        return line - off if line else None

    def visit(node, depth):
        report.max_loop_depth = max(report.max_loop_depth, depth)

        if isinstance(node, LOOP_TYPES) and depth >= 2:
            report.findings.append(Finding(
                "nested-loop", line_of(node),
                f"loop nested at depth {depth}"))

        if depth >= 1 and isinstance(node, T.MethodInvocation) \
                and node.member in ("contains", "indexOf", "remove"):
            report.findings.append(Finding(
                "linear-search-in-loop", line_of(node),
                f".{node.member}() called inside a loop "
                "(on a List this is itself O(n))"))

        if depth >= 1 and isinstance(node, T.Assignment) and node.type == "+=" \
                and isinstance(node.value, T.Literal) \
                and str(node.value.value).startswith('"'):
            report.findings.append(Finding(
                "string-concat-in-loop", line_of(node),
                "String built with += inside a loop (creates many objects)"))

        if isinstance(node, T.BinaryOperation) and node.operator in ("==", "!=") \
                and any(isinstance(s, T.Literal) and str(s.value).startswith('"')
                        for s in (node.operandl, node.operandr)):
            report.findings.append(Finding(
                "string-equality", line_of(node),
                "Strings compared with == / != instead of .equals()"))

        if isinstance(node, T.MethodDeclaration):
            for _, call in node.filter(T.MethodInvocation):
                if call.member == node.name and call.qualifier in (None, ""):
                    report.findings.append(Finding(
                        "recursion", line_of(node),
                        f"method '{node.name}' calls itself"))
                    break

    _walk(ast, 0, visit)
    return report
