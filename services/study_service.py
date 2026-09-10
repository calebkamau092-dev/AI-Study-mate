from repositories.progress_repository import ProgressRepository

class StudyService:
    def __init__(self, progress_repo: ProgressRepository = None):
        self.progress_repo = progress_repo or ProgressRepository()

    def record_quiz_result(self, username: str, topic: str, score: float):
        progress = self.progress_repo.get_user_progress(username)
        
        progress["quiz_history"].append({
            "topic": topic,
            "score": score
        })

        if topic not in progress["topic_scores"]:
            progress["topic_scores"][topic] = []
        progress["topic_scores"][topic].append(score)

        self.progress_repo.save_user_progress(username, progress)

    def get_weak_topics(self, username: str, threshold: float = 60.0) -> list:
        progress = self.progress_repo.get_user_progress(username)
        topic_scores = progress.get("topic_scores", {})
        
        weak_topics = []
        for topic, scores in topic_scores.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            if avg_score < threshold:
                weak_topics.append({"topic": topic, "average_score": round(avg_score, 2)})
        
        return weak_topics

    def get_performance_summary(self, username: str) -> dict:
        progress = self.progress_repo.get_user_progress(username)
        history = progress.get("quiz_history", [])
        
        total_quizzes = len(history)
        if total_quizzes == 0:
            return {"total_quizzes": 0, "overall_average": 0.0, "weak_topics": []}

        overall_avg = sum(item["score"] for item in history) / total_quizzes
        weak_topics = self.get_weak_topics(username)

        return {
            "total_quizzes": total_quizzes,
            "overall_average": round(overall_avg, 2),
            "weak_topics": weak_topics
        }

    def generate_study_plan(self, username: str) -> str:
        summary = self.get_performance_summary(username)
        weak_topics = summary["weak_topics"]

        plan = f"=== Study Plan for {username} ===\n"
        if not weak_topics:
            plan += "Great job! You currently have no identified weak topics.\n"
            plan += "Recommended Action: Review advanced Python concepts or take new quizzes."
            return plan

        plan += "Based on your quiz performance, focus on these weak areas:\n\n"
        for idx, item in enumerate(weak_topics, 1):
            plan += f"{idx}. Topic: {item['topic']} (Current Average: {item['average_score']}%)\n"
            plan += f"   - Action: Request AI explanations for '{item['topic']}'\n"
            plan += f"   - Practice: Complete a targeted quiz on '{item['topic']}'\n\n"
        
        return plan