"""
Tests for the Student and Subject models.

These tests check important behaviour such as:
    - creating subjects
    - managing topics
    - creating students
    - assigning subjects
    - recording quiz results
    - calculating average scores
    - tracking weak topics
    - rejecting invalid data
"""

import pytest

from models.student import Student
from models.subject import Subject


def test_create_python_subject():
    """
    A Subject should store its name correctly.
    """

    python_subject = Subject("Python")

    assert python_subject.name == "Python"


def test_subject_can_add_topics():
    """
    Topics should be added to the Python subject.
    """

    python_subject = Subject("Python")

    python_subject.add_topic("Functions")
    python_subject.add_topic("Classes")

    assert python_subject.topics == [
        "Functions",
        "Classes",
    ]


def test_subject_does_not_duplicate_topics():
    """
    The same topic should not be stored twice.
    """

    python_subject = Subject("Python")

    python_subject.add_topic("Functions")
    python_subject.add_topic("Functions")

    assert python_subject.topics == [
        "Functions"
    ]


def test_subject_can_remove_topic():
    """
    An existing topic should be removable.
    """

    python_subject = Subject("Python")

    python_subject.add_topic("Functions")
    python_subject.add_topic("Classes")

    python_subject.remove_topic("Functions")

    assert python_subject.topics == [
        "Classes"
    ]


def test_subject_can_check_topic():
    """
    has_topic() should return True or False.
    """

    python_subject = Subject("Python")

    python_subject.add_topic("Classes")

    assert python_subject.has_topic("Classes") is True
    assert python_subject.has_topic("Java") is False


def test_empty_subject_name_is_rejected():
    """
    A Subject should not accept an empty name.
    """

    with pytest.raises(ValueError):
        Subject("")


def test_student_can_be_created():
    """
    Student should store the username.
    """

    student = Student("julius")

    assert student.username == "julius"


def test_student_can_add_python_subject():
    """
    Student should be able to study Python.
    """

    student = Student("julius")

    python_subject = Subject("Python")

    student.add_subject(python_subject)

    assert student.get_subject(
        "Python"
    ) is python_subject


def test_student_starts_with_zero_average():
    """
    A student who has never completed a quiz
    should have an average score of 0.
    """

    student = Student("julius")

    assert student.average_score() == 0.0


def test_student_can_record_quiz_result():
    """
    Completed quiz results should be added
    to quiz history.
    """

    student = Student("julius")

    result = {
        "subject": "Python",
        "topic": "OOP",
        "correct_answers": 4,
        "total_questions": 5,
        "score": 80.0,
        "weak_topics": [
            "Inheritance"
        ],
    }

    student.record_quiz_result(result)

    assert len(student.quiz_history) == 1


def test_student_calculates_average_score():
    """
    Average score should be calculated from
    all completed quizzes.
    """

    student = Student("julius")

    first_result = {
        "subject": "Python",
        "topic": "Functions",
        "correct_answers": 4,
        "total_questions": 5,
        "score": 80.0,
        "weak_topics": [],
    }

    second_result = {
        "subject": "Python",
        "topic": "OOP",
        "correct_answers": 3,
        "total_questions": 5,
        "score": 60.0,
        "weak_topics": [
            "Inheritance"
        ],
    }

    student.record_quiz_result(first_result)
    student.record_quiz_result(second_result)

    assert student.average_score() == 70.0


def test_student_tracks_weak_topics():
    """
    Weak topics should be counted whenever
    they appear in quiz results.
    """

    student = Student("julius")

    first_result = {
        "subject": "Python",
        "topic": "OOP",
        "correct_answers": 4,
        "total_questions": 5,
        "score": 80.0,
        "weak_topics": [
            "Inheritance"
        ],
    }

    second_result = {
        "subject": "Python",
        "topic": "OOP",
        "correct_answers": 3,
        "total_questions": 5,
        "score": 60.0,
        "weak_topics": [
            "Inheritance",
            "Polymorphism",
        ],
    }

    student.record_quiz_result(first_result)
    student.record_quiz_result(second_result)

    assert student.weak_topics == {
        "Inheritance": 2,
        "Polymorphism": 1,
    }


def test_student_rejects_invalid_subject():
    """
    Student.add_subject() should only accept
    Subject objects.
    """

    student = Student("julius")

    with pytest.raises(TypeError):
        student.add_subject("Python")