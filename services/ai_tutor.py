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
        request_data = json.dumps(data).encode("utf-8")

        request = urllib.request.Request(
            self.url,
            data=request_data,
            headers={
                "Content-Type": "application/json"
            }
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=60
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

                return result.get("response", "").strip()

        except urllib.error.URLError:
            return None

        except Exception:
            return None

    # ---------------------------------
    # AI TOPIC EXPLANATION
    # ---------------------------------

    def explain_topic(self, topic):
        prompt = f"""
You are a Python programming tutor.

Explain the following Python topic
in simple language for a beginner.

Topic: {topic}

Include:

1. A simple definition
2. Important concepts
3. A Python code example
4. A short summary

Make the explanation clear and easy to understand.
"""

        response = self._ask_ollama(prompt)

        if response:
            return response

        return (
            "Unable to connect to the AI tutor. "
            "Please make sure Ollama is running."
        )

    # ---------------------------------
    # AI-GENERATED PYTHON QUIZ
    # ---------------------------------

    def generate_quiz(self, topic, number=5):
        prompt = f"""
You are a Python programming quiz developer.

Create {number} multiple-choice quiz questions
about the following Python topic:

{topic}

The questions should test understanding of Python.

Return ONLY valid JSON.

Use exactly this format:

[
    {{
        "question": "Question text",
        "options": {{
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
        }},
        "correct_answer": "A"
    }}
]

Rules:

- Create exactly {number} questions.
- Each question must have exactly four options.
- Only one option must be correct.
- Use Python examples where appropriate.
- The correct answer must be A, B, C, or D.
- Do not include explanations.
- Do not include markdown.
"""

        response = self._ask_ollama(prompt)

        if not response:
            return []

        try:
            response = response.replace(
                "```json", ""
            ).replace(
                "```", ""
            ).strip()

            questions = json.loads(response)

            return questions

        except json.JSONDecodeError:
            return []
