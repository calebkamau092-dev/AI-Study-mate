import json
import os

class ProgressRepository:
    def __init__(self, filepath="data/progress.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump({}, f)

    def load_all(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def get_user_progress(self, username):
        all_progress = self.load_all()
        return all_progress.get(username, {"quiz_history": [], "topic_scores": {}})

    def save_user_progress(self, username, progress_data):
        all_progress = self.load_all()
        all_progress[username] = progress_data
        with open(self.filepath, "w") as f:
            json.dump(all_progress, f, indent=4)