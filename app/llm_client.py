"""Provider-agnostic LLM client with tool-calling support, built on LiteLLM."""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

try:
    import litellm
    from litellm import acompletion
    from litellm.exceptions import (
        ServiceUnavailableError,
        RateLimitError,
        APIConnectionError,
        AuthenticationError,
        BadRequestError,
    )

    HAS_LITELLM = True
except Exception:
    litellm = None  # type: ignore[assignment]
    acompletion = None
    ServiceUnavailableError = Exception  # type: ignore[assignment,misc]
    RateLimitError = Exception  # type: ignore[assignment,misc]
    APIConnectionError = Exception  # type: ignore[assignment,misc]
    AuthenticationError = Exception  # type: ignore[assignment,misc]
    BadRequestError = Exception  # type: ignore[assignment,misc]
    HAS_LITELLM = False


SYSTEM_PROMPT = """You are a helpful kitchen assistant with access to the user's personal recipe collection and kitchen inventory.

You have tools to:
- List all recipes or get full details (steps + ingredients) for a specific one
- Calculate recipe costs and scale to any serving size
- View and update kitchen stock levels
- Create, update, and delete recipes and ingredients

Guidelines:
- Always use conversation history to understand follow-up questions. If the user says "show me that one", "how do I make it", or "what about the cost", look at previous messages to know what they're referring to.
- When a user asks about a specific recipe (steps, ingredients, how to make it), call get_recipe_details — not list_available_recipes.
- For general cooking knowledge (nutrition, techniques, substitutions, tips) answer directly without tools.
- Be concise and friendly. Don't repeat data the user didn't ask for."""

# Tool definitions exposed to the LLM.
# user_id is intentionally excluded — the agent injects it before calling the MCP tool.
KITCHEN_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_available_recipes",
            "description": "Returns a concise list of all the user's recipe names with yield info. Use this to browse the catalog or when unsure which recipe the user means.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recipe_details",
            "description": "Returns the full details of ONE specific recipe: preparation steps, yield, category, and ingredient list. Use this whenever the user asks about a specific recipe — how to make it, the steps, the ingredients, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string", "description": "Exact name of the recipe"},
                },
                "required": ["recipe_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recipe_ingredients",
            "description": "Lists all ingredients and quantities for a specific recipe with per-unit breakdowns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                },
                "required": ["recipe_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_recipe_cost",
            "description": "Calculates the total production cost and cost per unit for a recipe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                },
                "required": ["recipe_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scale_recipe",
            "description": "Calculates scaled ingredient quantities and total cost for a desired yield.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "target_amount": {"type": "number", "description": "Desired output quantity"},
                    "target_unit": {"type": "string", "description": "Unit for the output, e.g. 'portions', 'g', 'cookies'. Leave empty to use the recipe's default."},
                },
                "required": ["recipe_name", "target_amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_inventory_report",
            "description": "Returns all ingredients and their current stock levels.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_stock",
            "description": "Updates the stock quantity for an ingredient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "amount": {"type": "number"},
                    "mode": {"type": "string", "enum": ["set", "add", "reduce"]},
                },
                "required": ["name", "amount", "mode"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_ingredient",
            "description": "Adds a new ingredient to the kitchen catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "unit": {"type": "string", "description": "Unit of measure: g, kg, ml, L, tsp, tbsp, cup, oz, lb, unit"},
                    "cost": {"type": "number", "description": "Cost per unit"},
                },
                "required": ["name", "unit", "cost"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_ingredient_price",
            "description": "Updates the cost per unit of an existing ingredient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "new_cost": {"type": "number"},
                },
                "required": ["name", "new_cost"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_full_recipe",
            "description": "Creates a new recipe with optional ingredients.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string", "description": "Preparation steps / description"},
                    "yield_amount": {"type": "number"},
                    "yield_unit": {"type": "string"},
                    "ingredients": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "amount": {"type": "number"},
                                "unit": {"type": "string"},
                                "cost": {"type": "number"},
                            },
                            "required": ["name", "amount"],
                        },
                    },
                },
                "required": ["name", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_recipe",
            "description": "Updates a recipe's metadata: name, description, category, or yield.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "new_name": {"type": "string"},
                    "description": {"type": "string"},
                    "category": {"type": "string"},
                    "yield_amount": {"type": "number"},
                    "yield_unit": {"type": "string"},
                },
                "required": ["recipe_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_recipe",
            "description": "Permanently deletes a recipe and all its ingredient links.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                },
                "required": ["recipe_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_ingredient_to_recipe",
            "description": "Adds an ingredient to an existing recipe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "ingredient_name": {"type": "string"},
                    "amount": {"type": "number"},
                    "unit": {"type": "string"},
                    "cost": {"type": "number"},
                },
                "required": ["recipe_name", "ingredient_name", "amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_recipe_ingredient_quantity",
            "description": "Updates the quantity of a specific ingredient within a recipe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "ingredient_name": {"type": "string"},
                    "new_amount": {"type": "number"},
                },
                "required": ["recipe_name", "ingredient_name", "new_amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_ingredient_from_recipe",
            "description": "Removes an ingredient from a recipe without deleting it from the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "ingredient_name": {"type": "string"},
                },
                "required": ["recipe_name", "ingredient_name"],
            },
        },
    },
]


# Errors that mean "this provider can't serve right now" — skip to next in chain
_FALLBACK_ERRORS = (ServiceUnavailableError, RateLimitError, APIConnectionError, AuthenticationError, BadRequestError)


class LLMClient:
    """LLM client with tool-calling support and automatic provider fallback."""

    def __init__(self) -> None:
        self.model_chain = self._build_model_chain()
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    async def run_agent_turn(
        self,
        user_prompt: str,
        conversation_history: list[dict],
        tool_executor: Callable[[str, dict], Awaitable[str]],
    ) -> tuple[str, list[str]]:
        """Run a full agent turn, falling back across providers on transient errors.

        Returns:
            (reply_text, tools_used)
        """
        if not HAS_LITELLM or not self.model_chain:
            return "Language model is not configured.", []

        base_messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history,
            {"role": "user", "content": user_prompt},
        ]
        tools_used: list[str] = []

        last_error: Exception | None = None
        for model in self.model_chain:
            try:
                reply, tools_used = await self._run_with_model(
                    model, list(base_messages), tool_executor
                )
                if model != self.model_chain[0]:
                    logger.info("Succeeded with fallback model=%s", model)
                return reply, tools_used
            except _FALLBACK_ERRORS as exc:
                logger.warning("Model %s unavailable (%s), trying next fallback", model, exc)
                last_error = exc
            except Exception as exc:
                logger.warning("Model %s failed unexpectedly (%s), trying next fallback", model, exc)
                last_error = exc

        logger.error("All models in chain failed. Last error: %s", last_error)
        return "I'm having trouble right now. Please try again later.", tools_used

    async def _run_with_model(
        self,
        model: str,
        messages: list[dict[str, Any]],
        tool_executor: Callable[[str, dict], Awaitable[str]],
    ) -> tuple[str, list[str]]:
        tools_used: list[str] = []

        for _ in range(4):  # max tool-call rounds per turn
            response = await acompletion(  # type: ignore[misc]
                model=model,
                messages=messages,
                tools=KITCHEN_TOOLS,
                tool_choice="auto",
                temperature=self.temperature,
            )

            msg = response.choices[0].message
            tool_calls = getattr(msg, "tool_calls", None)

            if not tool_calls:
                return (msg.content or "").strip(), tools_used

            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in tool_calls
                ],
            })

            for tc in tool_calls:
                tool_name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments or "{}") or {}
                except json.JSONDecodeError:
                    args = {}

                tools_used.append(tool_name)
                result = await tool_executor(tool_name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

        return "I had trouble completing that request. Please try again.", tools_used

    @staticmethod
    def _build_model_chain() -> list[str]:
        """Build ordered list of available models from configured API keys."""
        chain: list[str] = []

        def _prefixed(model: str, prefix: str) -> str:
            return model if "/" in model else f"{prefix}/{model}"

        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if gemini_key:
            model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
            chain.append(_prefixed(model, "gemini"))

        if anthropic_key:
            model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
            chain.append(_prefixed(model, "anthropic"))

        if openai_key:
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            chain.append(_prefixed(model, "openai"))

        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            chain.append(_prefixed(model, "deepseek"))

        if not chain:
            chain.append("gemini/gemini-2.0-flash")

        logger.info("LLM model chain: %s", chain)
        return chain
