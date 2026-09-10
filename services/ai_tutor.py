import json
import urllib.request
import urllib.error


class AITutor:
    def __init__(
        self,
        model="llama3.2",
        url="http://localhost:11434/api/generate"
    ):
        self.model = model
        self.url = url

    def _ask_ollama(self, prompt):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

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