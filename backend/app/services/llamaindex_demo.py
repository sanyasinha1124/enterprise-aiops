"""
Optional LlamaIndex learning adapter.

The main RAG pipeline remains explicit and provider-visible. This file gives
you a starting point for learning how LlamaIndex represents documents and
nodes.
"""

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


def make_nodes(text: str):
    document = Document(text=text)
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=64)
    return parser.get_nodes_from_documents([document])


if __name__ == "__main__":
    nodes = make_nodes("EnterpriseOps AI uses RAG to retrieve relevant company knowledge.")
    print(f"Created {len(nodes)} nodes.")
