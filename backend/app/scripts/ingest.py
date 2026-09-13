from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = ROOT / "data" / "knowledge"


def chunk_text(text: str, chunk_size: int = 700) -> list[str]:
    words = re.split(r"\s+", text.strip())
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return [c for c in chunks if c]


def load_knowledge():
    records = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(chunk_text(text)):
            records.append(
                {
                    "title": path.stem.replace("_", " ").title(),
                    "source": path.name,
                    "chunk": idx,
                    "text": chunk,
                }
            )
    return records


if __name__ == "__main__":
    from app.services.rag import RAGService

    chunks = load_knowledge()
    count = RAGService().index_chunks(chunks)
    print(f"Indexed {count} chunks.")
