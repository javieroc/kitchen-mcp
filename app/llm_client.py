"""Provider-agnostic LLM formatting client built around LiteLLM."""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

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

    async def format_kitchen_response(
        self,
        user_prompt: str,
        factual_answer: str,
        conversation_history: list[dict] | None = None,
    ) -> str:
        """Rewrite factual tool output into concise, context-aware user-facing language."""
        if not factual_answer:
            return factual_answer

        if not HAS_LITELLM or not self._has_provider_credentials():
            return factual_answer

        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful kitchen assistant. Answer the user's question directly "
                    "and concisely using only the information in the tool output. "
                    "If the user asks about a specific recipe, extract and present only that "
                    "recipe's information. If the user asks for only names or titles, list only "
                    "the names. Do not invent facts that are not present in the tool output."
                ),
            },
            *(conversation_history or []),
            {
                "role": "user",
                "content": (
                    f"User request:\n{user_prompt}\n\n"
                    f"Tool data:\n{factual_answer}\n\n"
                    "Respond directly to the user's request using only the tool data above."
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
            logger.exception("LLM format_kitchen_response failed (model=%s)", self.model)
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
            logger.exception("LLM suggest_substitutions failed (model=%s)", self.model)

        return f"I couldn't generate substitutions for {ingredient} right now. Please try again."

    async def answer_general_kitchen_question(
        self,
        user_prompt: str,
        fallback_message: str,
        conversation_history: list[dict] | None = None,
    ) -> str:
        """Answer general kitchen questions when no specialized tool route matches."""
        if not HAS_LITELLM or not self._has_provider_credentials():
            return fallback_message

        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful kitchen assistant. Answer the user's question directly "
                    "with practical, concise guidance. You have access to the user's recipe "
                    "collection and kitchen inventory via tools (already called when needed). "
                    "Use the conversation history for context when answering follow-up questions."
                ),
            },
            *(conversation_history or []),
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
            logger.exception("LLM answer_general_kitchen_question failed (model=%s)", self.model)

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

        return "gemini/gemini-2.0-flash"

    @staticmethod
    def _has_provider_credentials() -> bool:
        return bool(
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
        )
