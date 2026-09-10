import json
import os

class UserRepository:
    def __init__(self, filepath="data/users.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def load_all(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_all(self, users_data):
        with open(self.filepath, "w") as f:
            json.dump(users_data, f, indent=4)

    def find_by_username(self, username):
        users = self.load_all()
        for user in users:
            if user.get("username") == username:
                return user
        return None

    def add_user(self, user_dict):
        users = self.load_all()
        users.append(user_dict)
        self.save_all(users)