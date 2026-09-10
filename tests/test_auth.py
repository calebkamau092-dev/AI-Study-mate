from services.ai_tutor import AITutor


def test_ai_tutor_creation():
    tutor = AITutor()

    assert tutor.model == "llama3.2"


def test_explain_topic(monkeypatch):
    tutor = AITutor()

    monkeypatch.setattr(
        tutor,
        "_ask_ollama",
        lambda prompt: "A Python list is an ordered collection."
    )

    result = tutor.explain_topic(
        "Python Lists"
    )

    assert "Python list" in result


def test_generate_quiz(monkeypatch):
    tutor = AITutor()

    fake_response = """
    [
        {
            "question": "Which method adds an item to a list?",
            "options": {
                "A": "pop()",
                "B": "append()",
                "C": "sort()",
                "D": "index()"
            },
            "correct_answer": "B"
        }
    ]
    """

    monkeypatch.setattr(
        tutor,
        "_ask_ollama",
        lambda prompt: fake_response
    )

    questions = tutor.generate_quiz(
        "Python Lists",
        1
    )

    assert len(questions) == 1
    assert questions[0]["correct_answer"] == "B"