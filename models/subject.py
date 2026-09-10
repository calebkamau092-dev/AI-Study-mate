"""
Subject Model
-------------

This file contains the Subject class for AI StudyMate.

AI StudyMate currently focuses on helping students learn Python.

The Subject class represents the Python subject and manages
the Python topics that a student can study.

Examples of Python topics include:
    - Variables
    - Data Types
    - Operators
    - Conditionals
    - Loops
    - Functions
    - Lists
    - Tuples
    - Dictionaries
    - Sets
    - Classes
    - Objects
    - Encapsulation
    - Inheritance
    - Polymorphism


OOP CONCEPTS USED
-----------------

1. Class
   Subject is the blueprint used to create subject objects.

2. Object
   Example:

       python_subject = Subject("Python")

3. Attributes
   Attributes store information about an object.

   In this class:
       self.name
       self._topics

4. Methods
   Methods represent what an object can do.

   Examples:
       add_topic()
       remove_topic()
       has_topic()
       topic_count()
       to_dict()

5. Encapsulation
   The _topics attribute should normally be changed using
   methods such as add_topic() rather than being changed
   directly from outside the class.

6. Validation
   Invalid subject names and topics are rejected before
   they can be stored.


RESPONSIBILITY
--------------

Subject handles subject-related information.

It does NOT:
    - ask the user for terminal input
    - communicate with Ollama
    - generate quiz questions
    - calculate quiz scores
    - save JSON files directly

Those responsibilities belong to other parts of AI StudyMate.
"""


class Subject:
    """
    Represent a subject that a student is studying.

    AI StudyMate currently uses Python as its subject.

    Example:

        python_subject = Subject("Python")
    """

    def __init__(self, name):
        """
        Create a new Subject object.

        __init__ runs automatically when a Subject
        object is created.

        Example:

            python_subject = Subject("Python")
        """

        # A subject name should be text.
        if not isinstance(name, str):
            raise TypeError("Subject name must be a string.")

        # Remove spaces before and after the name.
        #
        # "   Python   " becomes "Python".
        name = name.strip()

        # Prevent an empty subject name.
        if not name:
            raise ValueError("Subject name cannot be empty.")

        # Store the subject name inside the object.
        self.name = name

        # Store the topics belonging to the subject.
        #
        # The underscore shows that this attribute
        # should normally be managed through methods.
        self._topics = []

    @property
    def topics(self):
        """
        Return the topics in the subject.

        We return a copy so that another part of the
        program cannot accidentally modify _topics
        directly.
        """

        return self._topics.copy()

    def add_topic(self, topic):
        """
        Add a new topic.

        Example:

            python_subject.add_topic("Functions")
        """

        # Make sure the topic is text.
        if not isinstance(topic, str):
            raise TypeError("Topic must be a string.")

        # Remove unnecessary spaces.
        topic = topic.strip()

        # Reject an empty topic.
        if not topic:
            raise ValueError("Topic cannot be empty.")

        # Do not store duplicate topics.
        if topic not in self._topics:
            self._topics.append(topic)

    def remove_topic(self, topic):
        """
        Remove a topic from the subject.

        Example:

            python_subject.remove_topic("Functions")
        """

        if not isinstance(topic, str):
            raise TypeError("Topic must be a string.")

        topic = topic.strip()

        if not topic:
            raise ValueError("Topic cannot be empty.")

        # Do not attempt to remove something
        # that does not exist.
        if topic not in self._topics:
            raise ValueError(
                f"Topic '{topic}' does not exist in {self.name}."
            )

        self._topics.remove(topic)

    def has_topic(self, topic):
        """
        Check whether a topic exists.

        Returns:
            True  - topic exists
            False - topic does not exist
        """

        if not isinstance(topic, str):
            return False

        return topic.strip() in self._topics

    def topic_count(self):
        """
        Return the number of topics stored.

        Example:

            python_subject.topic_count()
        """

        return len(self._topics)

    def to_dict(self):
        """
        Convert this Subject object into a dictionary.

        This will help the repository layer later
        when saving data as JSON.

        Example result:

            {
                "name": "Python",
                "topics": [
                    "Functions",
                    "Classes"
                ]
            }
        """

        return {
            "name": self.name,
            "topics": self.topics,
        }

    def __str__(self):
        """
        Provide a readable representation of the object.

        Example:

            print(python_subject)

        Output:

            Python
        """

        return self.name