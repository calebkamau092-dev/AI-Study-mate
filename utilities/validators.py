def validate_name(name):
    """Check that the student's name is valid."""
    name = name.strip()

    if not name:
        return False, "Name cannot be empty."

    if len(name) < 2:
        return False, "Name must be at least 2 characters long."

    return True, name


def validate_username(username):
    """Check that the username is valid."""
    username = username.strip()

    if not username:
        return False, "Username cannot be empty."

    if len(username) < 3:
        return False, "Username must be at least 3 characters long."

    return True, username


def validate_password(password):
    """Check that the password is valid."""
    if not password:
        return False, "Password cannot be empty."

    if len(password) < 4:
        return False, "Password must be at least 4 characters long."

    return True, password


def validate_subject(subject):
    """Allow Python as the only supported study subject."""
    subject = subject.strip()

    if subject.lower() != "python":
        return False, "Only Python is supported as a study subject."

    return True, "Python"


def validate_topic(topic):
    """Check that a study topic is valid."""
    topic = topic.strip()

    if not topic:
        return False, "Topic cannot be empty."

    return True, topic


def get_menu_choice(prompt, minimum, maximum):
    """Get a valid number from a menu."""
    while True:
        choice = input(prompt).strip()

        try:
            choice = int(choice)

            if minimum <= choice <= maximum:
                return choice

            print(f"Please enter a number from {minimum} to {maximum}.")

        except ValueError:
            print("Invalid input. Please enter a number.")