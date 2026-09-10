import argparse

from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from utilities.validators import get_menu_choice, validate_topic


def show_welcome():
    """Display the application welcome message."""
    print("\n" + "=" * 50)
    print("              AI STUDYMATE")
    print("        Smart Learning Starts Here")
    print("=" * 50)


def show_main_menu():
    """Display the main menu."""
    print("\nMain Menu")
    print("-" * 30)
    print("1. Sign Up")
    print("2. Log In")
    print("3. Exit")


def signup(auth_service):
    """Handle student registration."""
    print("\n--- Sign Up ---")

    name = input("Enter your name: ")
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    success, message = auth_service.sign_up(
        name,
        username,
        password
    )

    print(f"\n{message}")

    if success:
        print("You can now log in.")


def login(auth_service):
    """Handle student login."""
    print("\n--- Log In ---")

    username = input("Username: ")
    password = input("Password: ")

    success, user, message = auth_service.login(
        username,
        password
    )

    print(f"\n{message}")

    if success:
        student_menu(user)

    return success


def student_menu(user):
    """Display the menu available after login."""

    while True:
        print("\n" + "=" * 50)
        print(f"Welcome, {user['name']}!")
        print("=" * 50)

        print("\nStudy Menu")
        print("-" * 30)
        print("1. Explain a Python Topic")
        print("2. Take a Python Quiz")
        print("3. Create a Study Plan")
        print("4. View Progress")
        print("5. Logout")

        choice = get_menu_choice(
            "\nChoose an option: ",
            1,
            5
        )

        if choice == 1:
            explain_topic()

        elif choice == 2:
            take_quiz()

        elif choice == 3:
            create_study_plan()

        elif choice == 4:
            view_progress()

        elif choice == 5:
            print("\nLogging out...")
            print("Thank you for using AI StudyMate!")
            break


def explain_topic():
    """Ask the AI tutor to explain a Python topic."""

    print("\n--- Explain a Python Topic ---")

    topic = input("Enter the Python topic you want explained: ")

    valid, result = validate_topic(topic)

    if not valid:
        print(result)
        return

    topic = result

    print(f"\nYou selected: {topic}")

    # The AI Tutor will be connected here.
    print("\nAI Tutor feature will generate your explanation here.")


def take_quiz():
    """Start a Python quiz."""

    print("\n--- Python Quiz ---")
    print("Your AI-generated Python quiz will appear here.")

    # Quiz functionality will be connected here.


def create_study_plan():
    """Create a study plan."""

    print("\n--- Study Plan ---")

    topic = input("What Python topic do you want to study? ")

    valid, result = validate_topic(topic)

    if not valid:
        print(result)
        return

    topic = result

    print(f"\nCreating a study plan for: {topic}")

    # AI Tutor study-plan functionality will be connected here.


def view_progress():
    """Display the student's learning progress."""

    print("\n--- My Progress ---")
    print("Your quiz scores and weak topics will appear here.")

    # Progress repository functionality will be connected here.


def create_parser():
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="AI StudyMate - AI-powered Python study assistant."
    )

    parser.add_argument(
        "--version",
        action="version",
        version="AI StudyMate 1.0"
    )

    return parser


def run_application():
    """Start the AI StudyMate application."""

    show_welcome()

    user_repository = UserRepository()
    auth_service = AuthService(user_repository)

    while True:
        show_main_menu()

        choice = get_menu_choice(
            "\nChoose an option: ",
            1,
            3
        )

        if choice == 1:
            signup(auth_service)

        elif choice == 2:
            login(auth_service)

        elif choice == 3:
            print("\nThank you for using AI StudyMate!")
            print("Goodbye!")
            break


def main():
    """Application entry point."""

    parser = create_parser()
    parser.parse_args()

    run_application()


if __name__ == "__main__":
    main()