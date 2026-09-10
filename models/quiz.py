"""
Quiz Model
----------

This file contains the Quiz class for AI StudyMate.

AI StudyMate currently focuses on Python.

The Quiz class is responsible for:
    - storing multiple-choice questions
    - validating quiz questions
    - validating student answers
    - checking correct and incorrect answers
    - calculating percentage scores
    - identifying weak Python topics
    - returning structured quiz results

The Quiz class does NOT generate questions using AI.

AI question generation belongs to the AITutor service.
"""


from models.subject import Subject


class Quiz:
    """
    Represent a Python multiple-choice quiz.

    Example:

        quiz = Quiz(
            subject=python_subject,
            topic="Functions",
            questions=questions
        )
    """

    def __init__(self, subject, topic, questions):
        """
        Create a new Quiz object.

        Parameters:
            subject:
                A Subject object. For AI StudyMate this
                will normally represent Python.

            topic:
                The main Python topic being tested.

            questions:
                A list containing multiple-choice
                question dictionaries.
        """

        # -------------------------------------------------
        # Validate the Subject object
        # -------------------------------------------------

        # Quiz should receive an actual Subject object,
        # rather than just the text "Python".
        if not isinstance(subject, Subject):
            raise TypeError(
                "subject must be a Subject object."
            )

        # -------------------------------------------------
        # Validate the quiz topic
        # -------------------------------------------------

        if not isinstance(topic, str):
            raise TypeError(
                "Quiz topic must be a string."
            )

        topic = topic.strip()

        if not topic:
            raise ValueError(
                "Quiz topic cannot be empty."
            )

        # -------------------------------------------------
        # Validate the question collection
        # -------------------------------------------------

        if not isinstance(questions, list):
            raise TypeError(
                "Quiz questions must be stored in a list."
            )

        if not questions:
            raise ValueError(
                "Quiz must contain at least one question."
            )

        # Store the Subject and topic.
        self.subject = subject
        self.topic = topic

        # Questions are stored internally.
        self._questions = []

        # Validate every question before storing it.
        for question in questions:
            validated_question = self._validate_question(
                question
            )

            self._questions.append(
                validated_question
            )

    @property
    def questions(self):
        """
        Return copies of the quiz questions.

        Returning copies helps protect the internal
        _questions collection from accidental changes.
        """

        return [
            {
                "question": question["question"],
                "options": question["options"].copy(),
                "correct_answer": question[
                    "correct_answer"
                ],
                "topic": question["topic"],
            }
            for question in self._questions
        ]

    @property
    def total_questions(self):
        """
        Return the number of questions in the quiz.
        """

        return len(self._questions)

    def _validate_question(self, question):
        """
        Validate one multiple-choice question.

        Expected structure:

            {
                "question": "...",
                "options": [
                    "...",
                    "...",
                    "...",
                    "..."
                ],
                "correct_answer": "A",
                "topic": "..."
            }

        The leading underscore indicates that this is an
        internal helper method.
        """

        # Each question must be represented
        # using a dictionary.
        if not isinstance(question, dict):
            raise TypeError(
                "Each quiz question must be a dictionary."
            )

        # These fields must exist.
        required_fields = {
            "question",
            "options",
            "correct_answer",
        }

        missing_fields = (
            required_fields - question.keys()
        )

        if missing_fields:
            raise ValueError(
                "Question is missing required fields: "
                + ", ".join(
                    sorted(missing_fields)
                )
            )

        # -------------------------------------------------
        # Validate question text
        # -------------------------------------------------

        question_text = question["question"]

        if not isinstance(question_text, str):
            raise TypeError(
                "Question text must be a string."
            )

        question_text = question_text.strip()

        if not question_text:
            raise ValueError(
                "Question text cannot be empty."
            )

        # -------------------------------------------------
        # Validate answer options
        # -------------------------------------------------

        options = question["options"]

        if not isinstance(options, list):
            raise TypeError(
                "Question options must be stored in a list."
            )

        # For the current AI StudyMate design,
        # every question has four options:
        #
        # A, B, C and D.
        if len(options) != 4:
            raise ValueError(
                "Each question must contain exactly four options."
            )

        clean_options = []

        for option in options:

            if not isinstance(option, str):
                raise TypeError(
                    "Every question option must be a string."
                )

            option = option.strip()

            if not option:
                raise ValueError(
                    "Question options cannot be empty."
                )

            clean_options.append(option)

        # -------------------------------------------------
        # Validate the correct answer
        # -------------------------------------------------

        correct_answer = question[
            "correct_answer"
        ]

        if not isinstance(correct_answer, str):
            raise TypeError(
                "Correct answer must be a letter."
            )

        # This allows:
        #
        # "a"
        #
        # to become:
        #
        # "A"
        correct_answer = (
            correct_answer.strip().upper()
        )

        valid_answers = [
            "A",
            "B",
            "C",
            "D",
        ]

        if correct_answer not in valid_answers:
            raise ValueError(
                "Correct answer must be A, B, C or D."
            )

        # -------------------------------------------------
        # Validate question topic
        # -------------------------------------------------

        # Individual questions may test a more specific
        # topic than the overall quiz.
        #
        # Example:
        #
        # Quiz topic:
        #     Object-Oriented Programming
        #
        # Question topics:
        #     Classes
        #     Objects
        #     Inheritance
        #
        # If no question-specific topic is supplied,
        # use the main quiz topic.
        question_topic = question.get(
            "topic",
            self.topic,
        )

        if not isinstance(question_topic, str):
            raise TypeError(
                "Question topic must be a string."
            )

        question_topic = question_topic.strip()

        if not question_topic:
            raise ValueError(
                "Question topic cannot be empty."
            )

        # Return a clean validated question.
        return {
            "question": question_text,
            "options": clean_options,
            "correct_answer": correct_answer,
            "topic": question_topic,
        }

    def _normalize_answer(self, answer):
        """
        Convert student input into a standard answer letter.

        The Quiz accepts:

            A
            B
            C
            D

        It also accepts lowercase:

            a
            b
            c
            d

        And numbers:

            1 -> A
            2 -> B
            3 -> C
            4 -> D
        """

        answer_letters = [
            "A",
            "B",
            "C",
            "D",
        ]

        # -------------------------------------------------
        # Integer input
        # -------------------------------------------------

        if isinstance(answer, int):

            if 1 <= answer <= 4:
                return answer_letters[
                    answer - 1
                ]

            raise ValueError(
                "Answer number must be between 1 and 4."
            )

        # -------------------------------------------------
        # String input
        # -------------------------------------------------

        if isinstance(answer, str):

            answer = answer.strip().upper()

            # Convert:
            #
            # "1" -> "A"
            # "2" -> "B"
            # etc.
            if answer.isdigit():

                number = int(answer)

                if 1 <= number <= 4:
                    return answer_letters[
                        number - 1
                    ]

            # Standard letter answer.
            if answer in answer_letters:
                return answer

        raise ValueError(
            "Answer must be A, B, C, D or a number from 1 to 4."
        )

    def grade(self, answers):
        """
        Grade the student's answers.

        Parameters:
            answers:
                A list containing one answer for each
                quiz question.

        Example:

            ["A", "C", "B", "D"]

        Returns:
            A dictionary containing:
                - subject
                - topic
                - correct answers
                - total questions
                - percentage score
                - weak topics
                - question-by-question details
        """

        if not isinstance(answers, list):
            raise TypeError(
                "Quiz answers must be stored in a list."
            )

        # There must be exactly one answer
        # for every question.
        if len(answers) != self.total_questions:
            raise ValueError(
                "Provide one answer for every quiz question."
            )

        correct_count = 0

        weak_topics = []

        details = []

        # zip() pairs each question with
        # the student's corresponding answer.
        for question_number, (
            question,
            student_answer,
        ) in enumerate(
            zip(
                self._questions,
                answers,
            ),
            start=1,
        ):

            # Convert input into A/B/C/D.
            selected_answer = (
                self._normalize_answer(
                    student_answer
                )
            )

            correct_answer = question[
                "correct_answer"
            ]

            # Compare student's answer with
            # the correct answer.
            is_correct = (
                selected_answer
                == correct_answer
            )

            if is_correct:

                correct_count += 1

            else:

                # If the question was answered
                # incorrectly, its topic becomes
                # a weak topic.
                weak_topics.append(
                    question["topic"]
                )

            # Store detailed information about
            # this individual question.
            details.append(
                {
                    "question_number": question_number,
                    "question": question[
                        "question"
                    ],
                    "selected_answer": selected_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                    "topic": question["topic"],
                }
            )

        # -------------------------------------------------
        # Calculate percentage score
        # -------------------------------------------------

        # Formula:
        #
        # correct answers
        # --------------- x 100
        # total questions
        #
        # Example:
        #
        # 4 / 5 x 100 = 80%
        score = round(
            (
                correct_count
                / self.total_questions
            )
            * 100,
            2,
        )

        # Remove duplicate weak topics while
        # keeping their original order.
        #
        # Example:
        #
        # ["Inheritance", "Inheritance", "Classes"]
        #
        # becomes:
        #
        # ["Inheritance", "Classes"]
        unique_weak_topics = list(
            dict.fromkeys(
                weak_topics
            )
        )

        # This result matches the structure expected
        # by Student.record_quiz_result().
        return {
            "subject": self.subject.name,
            "topic": self.topic,
            "correct_answers": correct_count,
            "total_questions": self.total_questions,
            "score": score,
            "weak_topics": unique_weak_topics,
            "details": details,
        }

    def to_dict(self):
        """
        Convert the Quiz object into a dictionary.

        This makes the quiz data easier to work with
        in services or repositories.
        """

        return {
            "subject": self.subject.name,
            "topic": self.topic,
            "questions": self.questions,
        }

    def __str__(self):
        """
        Return a readable description of the quiz.

        Example:

            Python Quiz - Functions
        """

        return (
            f"{self.subject.name} Quiz - {self.topic}"
        )