import json
import re
from typing import Any

from google import genai
from google.genai import types

from app.config import settings
from app.services.fallback import fallback_recommendation


_client = None


def get_gemini_client():
    global _client

    if _client is not None:
        return _client

    if not settings.GEMINI_API_KEY:
        return None

    try:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return _client
    except Exception:
        return None


def _clean_json_text(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    return text.strip()


def _parse_response(text: str) -> dict[str, Any] | None:
    try:
        cleaned = _clean_json_text(text)
        result = json.loads(cleaned)

        if isinstance(result, dict):
            return result

    except (json.JSONDecodeError, TypeError):
        return None

    return None


def _build_prompt(
    kind: str,
    data: dict[str, Any],
) -> str:
    return f"""
You are PocketSmart AI, a practical personal budget recommendation assistant.

Create a useful recommendation for the user.

Planner type:
{kind}

User information:
{json.dumps(data, indent=2, ensure_ascii=False)}

Important requirements:

1. Respect the user's budget.
2. Give realistic and practical suggestions.
3. Do not invent exact product availability.
4. Give approximate budget allocations where useful.
5. Keep the recommendation easy to understand.
6. Return ONLY valid JSON.
7. Do not use Markdown code fences.

Return this JSON structure:

{{
  "source": "gemini",
  "title": "short recommendation title",
  "summary": "short useful summary",
  "suggestions": [
    "suggestion 1",
    "suggestion 2",
    "suggestion 3",
    "suggestion 4",
    "suggestion 5"
  ],
  "budget_breakdown": {{
    "category 1": 0,
    "category 2": 0,
    "category 3": 0
  }},
  "tips": [
    "tip 1",
    "tip 2",
    "tip 3"
  ],
  "marketplace_searches": [
    "search phrase 1",
    "search phrase 2",
    "search phrase 3"
  ]
}}
""".strip()


def generate_recommendation(
    kind: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    fallback = fallback_recommendation(kind, data)

    client = get_gemini_client()

    if client is None:
        return fallback

    try:
        prompt = _build_prompt(kind, data)

        response = client.models.generate_content(
            model=settings.GEMINI_TEXT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            ),
        )

        response_text = getattr(response, "text", None)

        if not response_text:
            return fallback

        result = _parse_response(response_text)

        if not result:
            return fallback

        result["source"] = "gemini"

        if "title" not in result:
            result["title"] = fallback["title"]

        if "summary" not in result:
            result["summary"] = fallback["summary"]

        if "suggestions" not in result:
            result["suggestions"] = fallback["suggestions"]

        if "budget_breakdown" not in result:
            result["budget_breakdown"] = fallback["budget_breakdown"]

        if "tips" not in result:
            result["tips"] = fallback["tips"]

        if "marketplace_searches" not in result:
            result["marketplace_searches"] = fallback["marketplace_searches"]

        return result

    except Exception:
        return fallback


def generate_jewelry_image(
    prompt: str,
) -> tuple[bytes, str] | None:
    """
    Attempts to generate a jewelry outfit image.

    If the configured Gemini image model does not support image generation
    or the API call fails, None is returned so the main application
    continues working normally.
    """

    client = get_gemini_client()

    if client is None:
        return None

    if not settings.GEMINI_IMAGE_MODEL:
        return None

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        candidates = getattr(response, "candidates", None)

        if not candidates:
            return None

        for candidate in candidates:
            content = getattr(candidate, "content", None)

            if not content:
                continue

            parts = getattr(content, "parts", None)

            if not parts:
                continue

            for part in parts:
                inline_data = getattr(part, "inline_data", None)

                if not inline_data:
                    continue

                image_data = getattr(inline_data, "data", None)
                mime_type = getattr(
                    inline_data,
                    "mime_type",
                    "image/png",
                )

                if image_data:
                    return image_data, mime_type

    except Exception:
        return None

    return None