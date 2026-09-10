"""
Student Model
-------------

This file contains the Student class for AI StudyMate.

A Student represents the learner who uses the application.

AI StudyMate currently focuses on Python, so a student
will normally study the Python Subject object.

The Student class manages:
    - the student's username
    - subjects being studied
    - quiz history
    - weak Python topics
    - average quiz performance

Authentication is NOT handled here.
Password and login logic belong to AuthService.
"""

from models.subject import Subject


class Student:
    """
    Represent a student using AI StudyMate.

    Example:

        student = Student("julius")
    """

    def __init__(self, username):
        """
        Create a new Student object.

        Example:

            student = Student("julius")
        """

        # Username must be text.
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")

        # Remove unnecessary spaces.
        username = username.strip()

        # Do not allow an empty username.
        if not username:
            raise ValueError("Username cannot be empty.")

        self.username = username

        # Store Subject objects.
        #
        # A dictionary makes it easy to find a subject
        # using its name.
        #
        # Example:
        #
        # {
        #     "python": <Subject object>
        # }
        self._subjects = {}

        # Store previous quiz results.
        self._quiz_history = []

        # Keep track of topics where the student
        # has difficulty.
        #
        # Example:
        #
        # {
        #     "Inheritance": 2,
        #     "Dictionaries": 1
        # }
        #
        # The number represents how many times
        # the topic was identified as weak.
        self._weak_topics = {}

    @property
    def subjects(self):
        """
        Return the subjects being studied.

        We return a list instead of exposing the
        internal dictionary directly.
        """

        return list(self._subjects.values())

    @property
    def quiz_history(self):
        """
        Return a copy of the student's quiz history.
        """

        return [
            result.copy()
            for result in self._quiz_history
        ]

    @property
    def weak_topics(self):
        """
        Return a copy of weak-topic information.
        """

        return self._weak_topics.copy()

    def add_subject(self, subject):
        """
        Add a Subject object to the student.

        Example:

            python_subject = Subject("Python")
            student.add_subject(python_subject)
        """

        # The value must actually be a Subject object.
        if not isinstance(subject, Subject):
            raise TypeError(
                "subject must be a Subject object."
            )

        # Convert the subject name to lowercase for
        # consistent lookup.
        #
        # "Python" becomes "python".
        key = subject.name.casefold()

        # Store the Subject object.
        self._subjects[key] = subject

    def get_subject(self, subject_name):
        """
        Find a student's subject using its name.

        Example:

            student.get_subject("Python")
        """

        if not isinstance(subject_name, str):
            return None

        key = subject_name.strip().casefold()

        return self._subjects.get(key)

    def record_quiz_result(self, result):
        """
        Record the result of a completed quiz.

        Important:
        This method does NOT calculate the quiz score.

        The Quiz class will calculate the score.

        Student only stores the final result.

        Example result:

            {
                "subject": "Python",
                "topic": "OOP",
                "correct_answers": 4,
                "total_questions": 5,
                "score": 80.0,
                "weak_topics": ["Inheritance"]
            }
        """

        # The quiz result should be a dictionary.
        if not isinstance(result, dict):
            raise TypeError(
                "Quiz result must be a dictionary."
            )

        # These pieces of information must exist.
        required_fields = {
            "subject",
            "topic",
            "correct_answers",
            "total_questions",
            "score",
            "weak_topics",
        }

        missing_fields = required_fields - result.keys()

        if missing_fields:
            raise ValueError(
                "Quiz result is missing: "
                + ", ".join(sorted(missing_fields))
            )

        correct_answers = result["correct_answers"]
        total_questions = result["total_questions"]
        score = result["score"]

        # Validate question counts.
        if not isinstance(correct_answers, int):
            raise TypeError(
                "Correct answers must be an integer."
            )

        if not isinstance(total_questions, int):
            raise TypeError(
                "Total questions must be an integer."
            )

        if total_questions <= 0:
            raise ValueError(
                "Total questions must be greater than zero."
            )

        if correct_answers < 0:
            raise ValueError(
                "Correct answers cannot be negative."
            )

        if correct_answers > total_questions:
            raise ValueError(
                "Correct answers cannot exceed total questions."
            )

        # Score must be a percentage.
        if not isinstance(score, (int, float)):
            raise TypeError(
                "Score must be a number."
            )

        if score < 0 or score > 100:
            raise ValueError(
                "Score must be between 0 and 100."
            )

        weak_topics = result["weak_topics"]

        if not isinstance(weak_topics, list):
            raise TypeError(
                "Weak topics must be stored in a list."
            )

        # Create a clean result before saving it.
        stored_result = {
            "subject": result["subject"],
            "topic": result["topic"],
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "score": score,
            "weak_topics": weak_topics.copy(),
        }

        # Add the result to quiz history.
        self._quiz_history.append(stored_result)

        # Count each weak topic.
        for topic in weak_topics:

            if not isinstance(topic, str):
                continue

            topic = topic.strip()

            if not topic:
                continue

            self._weak_topics[topic] = (
                self._weak_topics.get(topic, 0) + 1
            )

    def average_score(self):
        """
        Calculate the student's average quiz score.

        Example scores:

            80
            60
            100

        Average:

            (80 + 60 + 100) / 3 = 80
        """

        # Avoid dividing by zero when the student
        # has not completed any quizzes.
        if not self._quiz_history:
            return 0.0

        total_score = sum(
            result["score"]
            for result in self._quiz_history
        )

        average = total_score / len(self._quiz_history)

        return round(average, 2)

    def to_dict(self):
        """
        Convert the Student object into a dictionary.

        The repository layer can later save this
        dictionary into JSON.
        """

        return {
            "username": self.username,

            "subjects": [
                subject.to_dict()
                for subject in self.subjects
            ],

            "quiz_history": self.quiz_history,

            "weak_topics": self.weak_topics,

            "average_score": self.average_score(),
        }

    def __str__(self):
        """
        Return a readable student representation.

        Example:

            print(student)

        Output:

            julius
        """

        return self.username