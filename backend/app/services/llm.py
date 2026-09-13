import json
from typing import Any

from google import genai

from app.core.config import get_settings


class GeminiService:
    """Small provider wrapper so the rest of the application is not tied to SDK details."""

    def __init__(self):
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Copy backend/.env.example to backend/.env "
                "and add your Gemini API key."
            )
        self.settings = settings
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate(
        self,
        prompt: str,
        system_instruction: str | None = None,
    ) -> str:
        full_input = prompt
        if system_instruction:
            full_input = (
                f"SYSTEM INSTRUCTIONS:\n{system_instruction}\n\n"
                f"USER INPUT:\n{prompt}"
            )

        interaction = self.client.interactions.create(
            model=self.settings.gemini_model,
            input=full_input,
        )
        return interaction.output_text or ""

    def generate_json(self, prompt: str) -> dict[str, Any]:
        response = self.generate(
            prompt + "\nReturn ONLY valid JSON. Do not wrap it in markdown."
        )
        return json.loads(response)
