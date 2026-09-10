import requests


class AITutor:
    def __init__(self, model="llama3.2", ollama_url="http://localhost:11434/api/generate"):
        self.model = model
        self.ollama_url = ollama_url

    def ask_ai(self, prompt):
        """Send a prompt to Ollama and return the AI response."""

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(
                self.ollama_url,
                json=data,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            return (
                "Unable to connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except requests.exceptions.Timeout:
            return "The AI took too long to respond. Please try again."

        except requests.exceptions.RequestException as error:
            return f"AI request failed: {error}"

    def explain_topic(self, subject, topic):
        """Generate a beginner-friendly explanation of a topic."""

        prompt = f"""
You are AI StudyMate, a friendly AI tutor.

Explain the following topic to a beginner.

Subject: {subject}
Topic: {topic}

Requirements:
- Use simple language.
- Explain the main idea clearly.
- Give a simple example.
- Break difficult ideas into smaller parts.
- Do not make the explanation unnecessarily long.

Start the explanation directly.
"""

        return self.ask_ai(prompt)

    def generate_quiz(self, subject, topic, number_of_questions):
        """Generate multiple-choice questions about a topic."""

        prompt = f"""
You are AI StudyMate, an educational AI tutor.

Create {number_of_questions} multiple-choice questions.

Subject: {subject}
Topic: {topic}

For every question provide:

Question:
A. option
B. option
C. option
D. option
Answer: A/B/C/D
Explanation: short explanation

Make the questions suitable for a student studying this topic.
Do not include questions outside the given topic.
"""

        return self.ask_ai(prompt)

    def create_study_plan(self, subjects, topics, study_days):
        """Generate a personalized study plan."""

        prompt = f"""
You are AI StudyMate, a helpful study planner.

Create a simple study plan for a student.

Subjects:
{subjects}

Topics:
{topics}

Available study days:
{study_days}

Requirements:
- Organize the plan by day.
- Distribute the subjects fairly.
- Include specific topics to study.
- Include revision time.
- Include quiz/practice time.
- Keep the plan realistic for a student.
- Use a clear and easy-to-read format.
"""

        return self.ask_ai(prompt)