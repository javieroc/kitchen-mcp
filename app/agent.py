"""Chat orchestration for kitchen assistant capabilities."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .llm_client import LLMClient
from .mcp_client import MCPKitchenClient


@dataclass
class AgentResult:
    """Agent response payload."""

    reply: str
    tools_used: list[str]


SUBSTITUTIONS: dict[str, list[str]] = {
    "egg": ["1 tbsp flaxseed meal + 3 tbsp water", "1/4 cup unsweetened applesauce"],
    "butter": ["same amount olive oil", "same amount coconut oil"],
    "milk": ["same amount oat milk", "same amount almond milk"],
    "sugar": ["same amount honey (reduce liquids)", "same amount maple syrup (reduce liquids)"],
    "flour": ["1:1 gluten-free flour blend", "oat flour (for soft bakes)"],
}

CONVERSIONS: dict[tuple[str, str], float] = {
    ("g", "kg"): 0.001,
    ("kg", "g"): 1000,
    ("ml", "L"): 0.001,
    ("L", "ml"): 1000,
    ("tsp", "tbsp"): 1 / 3,
    ("tbsp", "tsp"): 3,
    ("cup", "ml"): 240,
    ("oz", "g"): 28.3495,
    ("lb", "g"): 453.592,
}


def _extract_recipe_name(prompt: str) -> str | None:
    quoted = re.search(r'"([^"]+)"', prompt)
    if quoted:
        return quoted.group(1).strip()

    trailing = re.search(r"(?:for|of)\s+([a-zA-Z0-9 \-_]+)$", prompt.strip(), flags=re.IGNORECASE)
    if trailing:
        return trailing.group(1).strip()

    return None


def _extract_conversion(prompt: str) -> tuple[float, str, str] | None:
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(g|kg|ml|L|tsp|tbsp|cup|oz|lb)\s*(?:to|in)\s*(g|kg|ml|L|tsp|tbsp|cup|oz|lb)",
        prompt,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    value, src_unit, dst_unit = match.groups()
    return float(value), src_unit, dst_unit


def _extract_substitution_ingredient(prompt: str) -> str | None:
    patterns = [
        r"(?:substitutions?|substitute)\s+(?:for|of)\s+([a-zA-Z0-9 \-]+)",
        r"(?:replace|instead of)\s+([a-zA-Z0-9 \-]+)",
        r"([a-zA-Z0-9 \-]+)\s+(?:substitution|substitute)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip(" .,!?:;")
            if value:
                return value
    return None


llm_client = LLMClient()


async def process_chat_prompt(prompt: str, user_id: str, mcp_client: MCPKitchenClient) -> AgentResult:
    """Route kitchen prompts to MCP tools or local utilities."""
    normalized = prompt.lower()
    tools_used: list[str] = []

    if "inventory" in normalized or "stock" in normalized:
        tools_used.append("get_inventory_report")
        factual = await mcp_client.call_tool("get_inventory_report", {"user_id": user_id})
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    if "list recipes" in normalized or ("recipes" in normalized and "available" in normalized):
        tools_used.append("list_available_recipes")
        factual = await mcp_client.call_tool("list_available_recipes", {"user_id": user_id})
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    if "ingredients for" in normalized:
        recipe = _extract_recipe_name(prompt)
        if not recipe:
            return AgentResult(
                reply="Please specify a recipe name, e.g. ingredients for \"Margherita Pizza\".",
                tools_used=tools_used,
            )
        tools_used.append("get_recipe_ingredients")
        factual = await mcp_client.call_tool(
            "get_recipe_ingredients",
            {"recipe_name": recipe, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    if "cost" in normalized or "price" in normalized:
        recipe = _extract_recipe_name(prompt)
        if not recipe:
            return AgentResult(
                reply="Please specify a recipe name, e.g. cost of \"Margherita Pizza\".",
                tools_used=tools_used,
            )
        tools_used.append("calculate_recipe_cost")
        factual = await mcp_client.call_tool(
            "calculate_recipe_cost",
            {"recipe_name": recipe, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    if "scale" in normalized or "serving" in normalized:
        servings_match = re.search(r"(\d+)\s*(?:servings|serving|x)", normalized)
        servings = int(servings_match.group(1)) if servings_match else 2
        recipe = _extract_recipe_name(prompt)
        if not recipe:
            return AgentResult(
                reply="Please specify a recipe name, e.g. scale \"Margherita Pizza\" to 4 servings.",
                tools_used=tools_used,
            )
        tools_used.append("scale_recipe")
        factual = await mcp_client.call_tool(
            "scale_recipe",
            {"recipe_name": recipe, "servings": servings, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    if "substitut" in normalized:
        ingredient = _extract_substitution_ingredient(prompt)
        if not ingredient:
            for key in SUBSTITUTIONS:
                if key in normalized:
                    ingredient = key
                    break
        if not ingredient:
            return AgentResult(
                reply="Tell me which ingredient you need to replace, e.g. substitution for egg.",
                tools_used=tools_used,
            )
        if ingredient.lower() in SUBSTITUTIONS:
            options = ", ".join(SUBSTITUTIONS[ingredient.lower()])
            return AgentResult(reply=f"Substitutions for {ingredient}: {options}.", tools_used=tools_used)

        reply = await llm_client.suggest_substitutions(ingredient=ingredient, user_prompt=prompt)
        return AgentResult(reply=reply, tools_used=tools_used)

    if "convert" in normalized or re.search(r"\bto\b", normalized):
        parsed = _extract_conversion(prompt)
        if parsed:
            value, src_unit, dst_unit = parsed
            factor = CONVERSIONS.get((src_unit, dst_unit))
            if factor is None:
                return AgentResult(
                    reply=f"I can't convert {src_unit} to {dst_unit} yet.",
                    tools_used=tools_used,
                )
            converted = value * factor
            return AgentResult(reply=f"{value} {src_unit} = {converted:.2f} {dst_unit}.", tools_used=tools_used)

    if "calorie" in normalized or "calories" in normalized:
        return AgentResult(
            reply=(
                "Calorie counting is planned. Next step is adding nutrition fields or a nutrition table in Supabase "
                "and exposing MCP tools to compute calories per recipe."
            ),
            tools_used=tools_used,
        )

    fallback = (
        "I can help with stock, recipe ingredients, recipe costs, scaling servings, unit conversions, and substitutions. "
        "Ask a kitchen question in one of these areas."
    )
    return AgentResult(reply=fallback, tools_used=tools_used)
