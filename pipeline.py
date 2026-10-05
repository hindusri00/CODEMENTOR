from analyzer import analyze
from rag import Retriever
import llm

# Map static findings -> keywords that pull in the right teaching notes.
# (Raw code alone is a weak retrieval query; findings describe the *concept*.)
KIND_TO_QUERY = {
    "nested-loop": "nested loops time complexity O(n^2) hash set lookup",
    "linear-search-in-loop": "list contains indexOf linear search hash set time complexity",
    "string-concat-in-loop": "string concatenation StringBuilder immutable loop",
    "string-equality": "string equals == comparison",
    "recursion": "recursion base case memoization",
}


def review(code: str, retriever: Retriever, hint_level: int = 2) -> dict:
    report = analyze(code)                                    # 1. static analysis
    expansion = " ".join(KIND_TO_QUERY.get(f.kind, "") for f in report.findings)
    query = f"{expansion} {expansion} {report.to_text()} {code}"  # findings weigh more than raw code
    docs = retriever.search(query, k=3)                       # 2. RAG
    notes = "\n\n---\n\n".join(d.text for d in docs)
    result = llm.explain(code, report.to_text(), notes, hint_level)  # 3. LLM
    result["_static"] = report.to_text()
    result["_sources"] = [d.title for d in docs]
    return result
