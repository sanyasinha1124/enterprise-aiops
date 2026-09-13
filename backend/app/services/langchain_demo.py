"""
Optional learning adapter.

This file is intentionally small: use it after understanding the direct Gemini
implementation in llm.py and rag.py.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda


def build_demo_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an enterprise support assistant."),
            ("human", "{question}"),
        ]
    )

    # This demonstrates LangChain's runnable composition without hiding the
    # provider-specific Gemini code used by the main application.
    return prompt | RunnableLambda(lambda value: value)


if __name__ == "__main__":
    chain = build_demo_chain()
    print(chain.invoke({"question": "What is RAG?"}))
