"""Provider-agnostic LLM formatting client built around LiteLLM."""

from __future__ import annotations

import os
from typing import Any

try:
    from litellm import acompletion

    HAS_LITELLM = True
except Exception:
    acompletion = None
    HAS_LITELLM = False


class LLMClient:
    """Minimal LLM client wrapper to keep provider/model switching config-driven."""

    def __init__(self) -> None:
        self.model = self._resolve_model()
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    async def format_kitchen_response(self, user_prompt: str, factual_answer: str) -> str:
        """Optionally rewrite factual tool output into concise user-facing language."""
        if not factual_answer:
            return factual_answer

        if not HAS_LITELLM or not self._has_provider_credentials():
            return factual_answer

        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a kitchen assistant. Be concise and practical. "
                    "Do not invent facts that are not present in the tool output."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"User prompt:\n{user_prompt}\n\n"
                    f"Tool factual answer:\n{factual_answer}\n\n"
                    "Rewrite this as a direct helpful response."
                ),
            },
        ]

        try:
            response = await acompletion(  # type: ignore[misc]
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content
            return content.strip() if content else factual_answer
        except Exception:
            return factual_answer

    async def suggest_substitutions(self, ingredient: str, user_prompt: str = "") -> str:
        """Generate substitution ideas for any ingredient."""
        if not HAS_LITELLM or not self._has_provider_credentials():
            return f"I can't generate substitutions for {ingredient} right now because the language model is unavailable."

        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a practical kitchen assistant. Give 3 to 5 safe and common substitutions. "
                    "Keep it concise and include short usage notes."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Ingredient to replace: {ingredient}\n"
                    f"User context: {user_prompt}\n"
                    "Return plain text starting with 'Substitutions for <ingredient>:'"
                ),
            },
        ]

        try:
            response = await acompletion(  # type: ignore[misc]
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception:
            pass

        return f"I couldn't generate substitutions for {ingredient} right now. Please try again."

    async def answer_general_kitchen_question(self, user_prompt: str, fallback_message: str) -> str:
        """Answer general kitchen questions when no specialized tool route matches."""
        if not HAS_LITELLM or not self._has_provider_credentials():
            return fallback_message

        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful kitchen assistant. Answer the user's question directly with practical, "
                    "concise guidance. If the request needs recipe-, inventory-, or cost-specific data that you "
                    "do not have, be honest and offer the best general guidance you can."
                ),
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        try:
            response = await acompletion(  # type: ignore[misc]
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception:
            pass

        return fallback_message

    @staticmethod
    def _resolve_model() -> str:
        configured = os.getenv("LLM_MODEL")
        if configured:
            return configured

        # Backward compatibility with previous Gemini-only env var.
        legacy = os.getenv("GEMINI_MODEL")
        if legacy:
            if "/" in legacy:
                return legacy
            return f"gemini/{legacy}"

        return "gemini/gemini-2.5-flash"

    @staticmethod
    def _has_provider_credentials() -> bool:
        return bool(
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
        )
