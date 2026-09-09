"""
Tests for the Quiz model and scoring system.

These tests verify that the Quiz class can:

- create a valid Python quiz
- count quiz questions
- calculate scores correctly
- identify weak topics
- accept lowercase answers
- accept numeric answers
- reject missing answers
- reject invalid answers
- reject invalid quiz questions
- work together with the Student class
"""

import pytest

from models.quiz import Quiz
from models.student import Student
from models.subject import Subject


# ---------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------
#
# A pytest fixture creates reusable test data.
#
# Instead of creating the same Python Subject and question
# list inside every test, we define them once here.
# ---------------------------------------------------------


@pytest.fixture
def python_subject():
    """
    Create a Python Subject object for Quiz tests.
    """

    subject = Subject("Python")

    subject.add_topic("Functions")
    subject.add_topic("Classes")
    subject.add_topic("Objects")

    return subject


@pytest.fixture
def sample_questions():
    """
    Return sample Python multiple-choice questions.

    These are test questions only.

    In the finished AI StudyMate application,
    questions will eventually come from the AI Tutor/Ollama.
    """

    return [
        {
            "question": (
                "Which keyword is used to define "
                "a function in Python?"
            ),
            "options": [
                "func",
                "def",
                "function",
                "define",
            ],
            "correct_answer": "B",
            "topic": "Functions",
        },
        {
            "question": (
                "Which keyword is used to create "
                "a class in Python?"
            ),
            "options": [
                "object",
                "new",
                "class",
                "def",
            ],
            "correct_answer": "C",
            "topic": "Classes",
        },
        {
            "question": (
                "What does self normally refer to "
                "in an instance method?"
            ),
            "options": [
                "The current object",
                "The current module",
                "The parent class only",
                "The Python interpreter",
            ],
            "correct_answer": "A",
            "topic": "Objects",
        },
    ]


# ---------------------------------------------------------
# QUIZ CREATION TESTS
# ---------------------------------------------------------


def test_quiz_can_be_created(
    python_subject,
    sample_questions,
):
    """
    A valid Quiz object should store its
    subject and topic correctly.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    assert quiz.subject is python_subject

    assert quiz.topic == (
        "Python OOP and Functions"
    )


def test_quiz_counts_questions(
    python_subject,
    sample_questions,
):
    """
    Quiz.total_questions should return
    the number of quiz questions.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    assert quiz.total_questions == 3


# ---------------------------------------------------------
# SCORING TESTS
# ---------------------------------------------------------


def test_quiz_calculates_perfect_score(
    python_subject,
    sample_questions,
):
    """
    All correct answers should produce 100%.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["B", "C", "A"]
    )

    assert result["correct_answers"] == 3
    assert result["total_questions"] == 3
    assert result["score"] == 100.0


def test_quiz_calculates_partial_score(
    python_subject,
    sample_questions,
):
    """
    Two correct answers out of three should
    produce approximately 66.67%.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["B", "A", "A"]
    )

    assert result["correct_answers"] == 2

    assert result["score"] == 66.67


# ---------------------------------------------------------
# WEAK TOPIC TESTS
# ---------------------------------------------------------


def test_quiz_identifies_weak_topic(
    python_subject,
    sample_questions,
):
    """
    If the student answers the Classes
    question incorrectly, Classes should
    appear as a weak topic.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["B", "A", "A"]
    )

    assert result["weak_topics"] == [
        "Classes"
    ]


def test_perfect_score_has_no_weak_topics(
    python_subject,
    sample_questions,
):
    """
    A perfect score should produce
    no weak topics.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["B", "C", "A"]
    )

    assert result["weak_topics"] == []


# ---------------------------------------------------------
# ANSWER NORMALIZATION TESTS
# ---------------------------------------------------------


def test_quiz_accepts_lowercase_answers(
    python_subject,
    sample_questions,
):
    """
    Lowercase answers should be accepted.

    Example:
        b -> B
        c -> C
        a -> A
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["b", "c", "a"]
    )

    assert result["score"] == 100.0


def test_quiz_accepts_numeric_answers(
    python_subject,
    sample_questions,
):
    """
    Numeric options should also work.

    Mapping:
        1 -> A
        2 -> B
        3 -> C
        4 -> D
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        [2, 3, 1]
    )

    assert result["score"] == 100.0


def test_quiz_accepts_numeric_string_answers(
    python_subject,
    sample_questions,
):
    """
    String numbers such as "2" should
    also be accepted.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["2", "3", "1"]
    )

    assert result["score"] == 100.0


# ---------------------------------------------------------
# INVALID INPUT TESTS
# ---------------------------------------------------------


def test_quiz_rejects_missing_answers(
    python_subject,
    sample_questions,
):
    """
    There must be one answer for every question.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    with pytest.raises(ValueError):
        quiz.grade(
            ["B", "C"]
        )


def test_quiz_rejects_invalid_answer(
    python_subject,
    sample_questions,
):
    """
    Answers outside A-D or 1-4
    should be rejected.
    """

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    with pytest.raises(ValueError):
        quiz.grade(
            ["B", "Z", "A"]
        )


def test_quiz_rejects_empty_question_list(
    python_subject,
):
    """
    A Quiz must contain at least one question.
    """

    with pytest.raises(ValueError):
        Quiz(
            python_subject,
            "Functions",
            [],
        )


def test_quiz_rejects_invalid_subject(
    sample_questions,
):
    """
    Quiz should receive a Subject object,
    not just the string "Python".
    """

    with pytest.raises(TypeError):
        Quiz(
            "Python",
            "Functions",
            sample_questions,
        )


def test_quiz_rejects_question_with_wrong_number_of_options(
    python_subject,
):
    """
    Our current quiz format requires
    exactly four options: A, B, C and D.
    """

    bad_questions = [
        {
            "question": (
                "Which keyword defines a function?"
            ),
            "options": [
                "func",
                "def",
                "function",
            ],
            "correct_answer": "B",
            "topic": "Functions",
        }
    ]

    with pytest.raises(ValueError):
        Quiz(
            python_subject,
            "Functions",
            bad_questions,
        )


def test_quiz_rejects_invalid_correct_answer(
    python_subject,
):
    """
    Correct answer must be A, B, C or D.
    """

    bad_questions = [
        {
            "question": (
                "Which keyword defines a function?"
            ),
            "options": [
                "func",
                "def",
                "function",
                "define",
            ],
            "correct_answer": "Z",
            "topic": "Functions",
        }
    ]

    with pytest.raises(ValueError):
        Quiz(
            python_subject,
            "Functions",
            bad_questions,
        )


# ---------------------------------------------------------
# STUDENT + QUIZ INTEGRATION TEST
# ---------------------------------------------------------


def test_quiz_result_can_be_recorded_by_student(
    python_subject,
    sample_questions,
):
    """
    This test proves that RAMCJ-10 Quiz results
    work with the Student class created in RAMCJ-9.
    """

    student = Student("julius")

    student.add_subject(
        python_subject
    )

    quiz = Quiz(
        python_subject,
        "Python OOP and Functions",
        sample_questions,
    )

    result = quiz.grade(
        ["B", "A", "A"]
    )

    student.record_quiz_result(
        result
    )

    assert len(
        student.quiz_history
    ) == 1

    assert student.average_score() == 66.67

    assert student.weak_topics == {
        "Classes": 1
    }