import time

from app.services.rag import RAGService


TEST_CASES = [
    {
        "question": "What is the refund window?",
        "keywords": ["30 days"],
    },
    {
        "question": "How long does standard shipping take?",
        "keywords": ["5", "7"],
    },
]


def run():
    rag = RAGService()
    passed = 0
    latencies = []

    for case in TEST_CASES:
        start = time.perf_counter()
        answer, _ = rag.answer(case["question"])
        latency = time.perf_counter() - start
        latencies.append(latency)

        answer_lower = answer.lower()
        ok = all(k.lower() in answer_lower for k in case["keywords"])
        passed += int(ok)

        print("=" * 70)
        print(case["question"])
        print(answer)
        print("PASS" if ok else "FAIL")
        print(f"Latency: {latency:.2f}s")

    print("=" * 70)
    print(f"Keyword pass rate: {passed / len(TEST_CASES):.2%}")
    print(f"Average latency: {sum(latencies) / len(latencies):.2f}s")


if __name__ == "__main__":
    run()
