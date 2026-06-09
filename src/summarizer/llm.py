"""LLM gateway.

`generate_text` is the single public entry point (it's the default `_generate`
collaborator in core.summarize). It dispatches to a backend based on the
`LLM_PROVIDER` env var:

  - "gemini" (default): Google Gemini via the google-genai SDK.
  - "ollama": a local Ollama server over HTTP (stdlib only, no extra deps).

Adding a backend means adding a `_generate_*` function and a branch here; core
and the tests stay backend-agnostic because they only see `generate_text`.
"""

import http.client
import json
import os
from typing import Optional

from google import genai


DEFAULT_PROVIDER = "gemini"

# --- Gemini --------------------------------------------------------------
GEMINI_DEFAULT_MODEL = "gemini-3.5-flash"

# --- Ollama --------------------------------------------------------------
OLLAMA_DEFAULT_MODEL = "qwen3.5"
OLLAMA_DEFAULT_HOST = "localhost"
OLLAMA_DEFAULT_PORT = 11434

DEFAULT_PROMPT = "Explain how AI works in a few words"


def get_provider() -> str:
    return os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER).strip().lower()


def get_api_key() -> Optional[str]:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def get_model_name() -> str:
    """Model recorded in the audit trail and sent to the active provider."""
    if get_provider() == "ollama":
        return os.getenv("OLLAMA_MODEL", OLLAMA_DEFAULT_MODEL)
    return os.getenv("GEMINI_MODEL", GEMINI_DEFAULT_MODEL)


def generate_text(prompt: str = DEFAULT_PROMPT) -> str:
    provider = get_provider()
    if provider == "ollama":
        return _generate_ollama(prompt)
    if provider == "gemini":
        return _generate_gemini(prompt)
    raise ValueError(
        f"Unknown LLM_PROVIDER {provider!r}. Expected 'gemini' or 'ollama'."
    )


def _generate_gemini(prompt: str) -> str:
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


def _generate_ollama(prompt: str) -> str:
    host = os.getenv("OLLAMA_HOST", OLLAMA_DEFAULT_HOST)
    port = int(os.getenv("OLLAMA_PORT", str(OLLAMA_DEFAULT_PORT)))

    payload = json.dumps(
        {
            "model": get_model_name(),
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
    )
    conn = http.client.HTTPConnection(host, port)
    try:
        conn.request(
            "POST", "/api/chat", payload, {"Content-Type": "application/json"}
        )
        response = conn.getresponse()
        body = response.read().decode()
        if response.status != 200:
            raise RuntimeError(
                f"Ollama returned HTTP {response.status}: {body[:200]}"
            )
    finally:
        conn.close()

    data = json.loads(body)
    return data["message"]["content"]
