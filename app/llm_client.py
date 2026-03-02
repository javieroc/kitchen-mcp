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
        normalized = ingredient.strip().lower()
        fallback_map: dict[str, list[str]] = {
            "pasta": ["zucchini noodles", "spaghetti squash", "shirataki noodles", "rice noodles"],
            "rice": ["quinoa", "cauliflower rice", "bulgur"],
            "bread": ["lettuce wraps", "whole grain tortillas", "rice cakes"],
            "cheese": ["nutritional yeast", "tofu ricotta", "cashew cream"],
            "cream": ["greek yogurt", "coconut cream", "evaporated milk"],
            "egg": ["1 tbsp flaxseed meal + 3 tbsp water", "1/4 cup unsweetened applesauce"],
            "butter": ["same amount olive oil", "same amount coconut oil"],
            "milk": ["same amount oat milk", "same amount almond milk"],
            "sugar": ["same amount honey (reduce liquids)", "same amount maple syrup (reduce liquids)"],
            "flour": ["1:1 gluten-free flour blend", "oat flour (for soft bakes)"],
        }

        for key, options in fallback_map.items():
            if key in normalized:
                return f"Substitutions for {ingredient}: {', '.join(options)}."

        if not HAS_LITELLM or not self._has_provider_credentials():
            return (
                f"Substitutions for {ingredient}: use an ingredient with similar function "
                "(starch, protein, fat, or acidity) and test in small batches."
            )

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

        return (
            f"Substitutions for {ingredient}: use an ingredient with similar function "
            "(starch, protein, fat, or acidity) and test in small batches."
        )

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
