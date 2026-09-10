"""
Tests for the Quiz model.
"""

import pytest

from models.quiz import Quiz
from models.student import Student
from models.subject import Subject


# -------------------------
# FIXTURES
# -------------------------

@pytest.fixture
def python_subject():
    subject = Subject("Python")
    subject.add_topic("Functions")
    subject.add_topic("Classes")
    subject.add_topic("Objects")
    return subject


@pytest.fixture
def sample_questions():
    return [
        {
            "question": "Which keyword defines a function?",
            "options": ["func", "def", "function", "define"],
            "correct_answer": "B",
            "topic": "Functions",
        },
        {
            "question": "Which keyword creates a class?",
            "options": ["object", "new", "class", "def"],
            "correct_answer": "C",
            "topic": "Classes",
        },
        {
            "question": "What does self refer to?",
            "options": [
                "The current object",
                "The current module",
                "The parent class",
                "The Python interpreter",
            ],
            "correct_answer": "A",
            "topic": "Objects",
        },
    ]


# -------------------------
# QUIZ CREATION
# -------------------------

def test_quiz_creation(python_subject, sample_questions):
    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    assert quiz.subject is python_subject
    assert quiz.topic == "Python OOP and Functions"
    assert quiz.total_questions == 3


# -------------------------
# SCORING
# -------------------------

@pytest.mark.parametrize(
    "answers, correct, score",
    [
        (["B", "C", "A"], 3, 100.0),
        (["B", "A", "A"], 2, 66.67),
    ],
)
def test_quiz_scoring(
    python_subject,
    sample_questions,
    answers,
    correct,
    score,
):
    quiz = Quiz(
        python_subject,
        "Python",
        sample_questions,
    )

    result = quiz.grade(answers)

    assert result["correct_answers"] == correct
    assert result["score"] == score


# -------------------------
# WEAK TOPICS
# -------------------------

def test_weak_topics(python_subject, sample_questions):
    quiz = Quiz(
        python_subject,
        "Python",
        sample_questions,
    )

    result = quiz.grade(["B", "A", "A"])

    assert result["weak_topics"] == ["Classes"]


def test_perfect_score_has_no_weak_topics(
    python_subject,
    sample_questions,
):
    quiz = Quiz(
        python_subject,
        "Python",
        sample_questions,
    )

    result = quiz.grade(["B", "C", "A"])

    assert result["weak_topics"] == []


# -------------------------
# ANSWER NORMALIZATION
# -------------------------

@pytest.mark.parametrize(
    "answers",
    [
        ["B", "C", "A"],
        ["b", "c", "a"],
        [2, 3, 1],
        ["2", "3", "1"],
    ],
)
def test_answer_formats(
    python_subject,
    sample_questions,
    answers,
):
    quiz = Quiz(
        python_subject,
        "Python",
        sample_questions,
    )

    assert quiz.grade(answers)["score"] == 100.0


# -------------------------
# INVALID INPUTS
# -------------------------

@pytest.mark.parametrize(
    "answers",
    [
        ["B", "C"],       # Missing answer
        ["B", "Z", "A"],  # Invalid answer
    ],
)
def test_invalid_answers(
    python_subject,
    sample_questions,
    answers,
):
    quiz = Quiz(
        python_subject,
        "Python",
        sample_questions,
    )

    with pytest.raises(ValueError):
        quiz.grade(answers)


def test_empty_question_list(python_subject):
    with pytest.raises(ValueError):
        Quiz(
            python_subject,
            "Python",
            [],
        )


def test_invalid_subject(sample_questions):
    with pytest.raises(TypeError):
        Quiz(
            "Python",
            "Python",
            sample_questions,
        )


def test_wrong_number_of_options(python_subject):
    bad_questions = [
        {
            "question": "Which keyword defines a function?",
            "options": ["func", "def", "function"],
            "correct_answer": "B",
            "topic": "Functions",
        }
    ]

    with pytest.raises(ValueError):
        Quiz(
            python_subject,
            "Python",
            bad_questions,
        )


def test_invalid_correct_answer(python_subject):
    bad_questions = [
        {
            "question": "Which keyword defines a function?",
            "options": ["func", "def", "function", "define"],
            "correct_answer": "Z",
            "topic": "Functions",
        }
    ]

    with pytest.raises(ValueError):
        Quiz(
            python_subject,
            "Python",
            bad_questions,
        )


# -------------------------
# STUDENT + QUIZ
# -------------------------

def test_student_quiz_integration(
    python_subject,
    sample_questions,
):
    student = Student("julius")
    student.add_subject(python_subject)

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(["B", "A", "A"])

    student.record_quiz_result(result)

    assert len(student.quiz_history) == 1
    assert student.average_score() == 66.67
    assert student.weak_topics == {"Classes": 1}