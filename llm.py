import os
from typing import Optional

from google import genai


DEFAULT_MODEL = "gemini-3.5-flash"
DEFAULT_PROMPT = "Explain how AI works in a few words"


def get_api_key() -> Optional[str]:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL)


def generate_text(prompt: str = DEFAULT_PROMPT) -> str:
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment or .env file."
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=get_model_name(),
        contents=prompt,
    )
    return response.text
