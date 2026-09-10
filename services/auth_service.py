from utilities.validators import (
    validate_name,
    validate_username,
    validate_password,
)


class AuthService:
    """Handles student registration and login."""

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def sign_up(self, name, username, password):
        """Create a new student account."""

        valid, result = validate_name(name)

        if not valid:
            return False, result

        name = result

        valid, result = validate_username(username)

        if not valid:
            return False, result

        username = result

        valid, result = validate_password(password)

        if not valid:
            return False, result

        password = result

        existing_user = self.user_repository.find_by_username(username)

        if existing_user:
            return False, "Username already exists."

        user = {
            "name": name,
            "username": username,
            "password": password
        }

        self.user_repository.add_user(user)

        return True, "Account created successfully."

    def login(self, username, password):
        """Log a student into the application."""

        username = username.strip()

        if not username:
            return False, None, "Username cannot be empty."

        if not password:
            return False, None, "Password cannot be empty."

        user = self.user_repository.find_by_username(username)

        if not user:
            return False, None, "Username not found."

        if user["password"] != password:
            return False, None, "Incorrect password."

        return True, user, "Login successful."