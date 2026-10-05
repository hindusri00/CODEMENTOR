"""Tiny RAG layer: retrieve relevant teaching notes from ./knowledge.

Uses TF-IDF (no embedding API needed). To upgrade later, swap `Retriever`
for one backed by sentence-transformers + FAISS/Chroma - same interface.
"""
from dataclasses import dataclass
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KB_DIR = Path(__file__).parent / "knowledge"


@dataclass
class Doc:
    title: str
    text: str


class Retriever:
    def __init__(self, kb_dir: Path = KB_DIR):
        self.docs: list[Doc] = []
        for p in sorted(kb_dir.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            title = text.splitlines()[0].lstrip("# ").strip()
            self.docs.append(Doc(title, text))
        self.vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vec.fit_transform(d.text for d in self.docs)

    def search(self, query: str, k: int = 3, min_score: float = 0.05) -> list[Doc]:
        scores = cosine_similarity(self.vec.transform([query]), self.matrix)[0]
        ranked = sorted(zip(scores, self.docs), key=lambda x: -x[0])
        return [d for s, d in ranked[:k] if s >= min_score]
