from chatbot_app.core.retriever import get_answer


def test_get_answer_returns_best_chunk():
    chunks = [
        "The capital of France is Paris.",
        "The capital of Germany is Berlin.",
    ]

    answer, relevant = get_answer("What is the capital of France?", chunks)

    assert answer == chunks[0]
    assert relevant[0] == chunks[0]
