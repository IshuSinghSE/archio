# ai_processor.py
import ollama
from config import OLLAMA_MODEL

class AIProcessor:
    """Handles translation from natural language to shell commands using a local LLM."""
    def __init__(self, model: str = OLLAMA_MODEL):
        self._model = model
        self._system_prompt = (
            "You are an expert at analyzing user requests and converting them into structured JSON output. "
            "Identify the user's primary intent and any relevant entities (parameters). "
            "Your response MUST be only a single JSON object with two keys: 'intent' and 'entities'. "
            "The 'entities' key should be a dictionary of parameters. "
            "Only output the command itself, with no explanation or extra text."
        )
        print(f"✅ AIProcessor initialized with model '{self._model}'.")

    def translate_to_command(self, natural_language_request: str) -> str:
        """Uses the local LLM to translate a request into a shell command."""
        try:
            response = ollama.chat(
                model=self._model,
                messages=[
                    {'role': 'system', 'content': self._system_prompt},
                    {'role': 'user', 'content': natural_language_request},
                ],
                options={'temperature': 0.0}
            )
            command = response['message']['content'].strip().replace("'", "")
            print(f"🧠 AI Suggested Command: '{command}'")
            return command
        except Exception as e:
            print(f"❌ Error communicating with local AI model: {e}")
            return ""