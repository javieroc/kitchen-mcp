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


def _extract_ingredient_name(prompt: str) -> str | None:
    """Extract a single ingredient name from the prompt."""
    patterns = [
        r'"([^"]+)"',
        r"(?:ingredient|stock|price|cost)\s+(?:for|of)\s+([a-zA-Z0-9 \-_]+?)(?:\s+to|\s+from|\s*$)",
        r"(?:add|update|remove|delete|reduce|set)\s+(?:ingredient\s+)?([a-zA-Z0-9 \-_]+?)(?:\s+(?:to|from|in|price|cost|stock|ingredient)|\s*$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip(" .,!?:;")
            if value:
                return value
    return None


def _extract_amount(prompt: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)", prompt)
    return float(match.group(1)) if match else None


def _extract_stock_mode(prompt: str) -> str:
    normalized = prompt.lower()
    if any(w in normalized for w in ("reduce", "use", "consume", "subtract")):
        return "reduce"
    if any(w in normalized for w in ("add", "receive", "restock", "increase")):
        return "add"
    return "set"


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

    # --- Mutations must be checked before reads to avoid mis-routing ---

    # update stock (before generic "stock" check)
    if re.search(r"\b(update|add|reduce|set|restock|receive|consume)\b.{0,20}\bstock\b", normalized) or \
       re.search(r"\bstock\b.{0,20}\b(update|add|reduce|set)\b", normalized):
        ingredient = _extract_ingredient_name(prompt)
        amount = _extract_amount(prompt)
        if not ingredient or amount is None:
            return AgentResult(
                reply='Please specify ingredient and amount, e.g. "add 500 to stock of Flour".',
                tools_used=tools_used,
            )
        mode = _extract_stock_mode(prompt)
        tools_used.append("update_stock")
        factual = await mcp_client.call_tool(
            "update_stock",
            {"name": ingredient, "amount": amount, "mode": mode, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # add ingredient to catalog
    if re.search(r"\b(add|create|new)\b.{0,20}\bingredient\b", normalized) and "to recipe" not in normalized and "to the recipe" not in normalized:
        ingredient = _extract_ingredient_name(prompt)
        if not ingredient:
            return AgentResult(
                reply='Please specify the ingredient name, e.g. "add ingredient Olive Oil, unit ml, cost 0.02".',
                tools_used=tools_used,
            )
        unit_match = re.search(r"\bunit\s*[:\s]+(\w+)", normalized)
        cost_match = re.search(r"\bcost\s*[:\s]+(\d+(?:\.\d+)?)", normalized)
        unit = unit_match.group(1) if unit_match else "unit"
        cost = float(cost_match.group(1)) if cost_match else 0.0
        tools_used.append("add_ingredient")
        factual = await mcp_client.call_tool(
            "add_ingredient",
            {"name": ingredient, "unit": unit, "cost": cost, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # update ingredient price/cost
    if re.search(r"\b(update|change|set)\b.{0,20}\b(price|cost)\b", normalized):
        ingredient = _extract_ingredient_name(prompt)
        new_cost = _extract_amount(prompt)
        if not ingredient or new_cost is None:
            return AgentResult(
                reply='Please specify ingredient and new cost, e.g. "update price of Flour to 0.03".',
                tools_used=tools_used,
            )
        tools_used.append("update_ingredient_price")
        factual = await mcp_client.call_tool(
            "update_ingredient_price",
            {"name": ingredient, "new_cost": new_cost, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # delete recipe
    if re.search(r"\b(delete|remove)\b.{0,20}\brecipe\b", normalized):
        recipe = _extract_recipe_name(prompt)
        if not recipe:
            return AgentResult(
                reply='Please specify the recipe name, e.g. delete recipe "Margherita Pizza".',
                tools_used=tools_used,
            )
        tools_used.append("delete_recipe")
        factual = await mcp_client.call_tool(
            "delete_recipe",
            {"recipe_name": recipe, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # update recipe metadata
    if re.search(r"\b(update|rename|edit)\b.{0,20}\brecipe\b", normalized):
        recipe = _extract_recipe_name(prompt)
        if not recipe:
            return AgentResult(
                reply='Please specify the recipe name, e.g. rename recipe "Old Name" to "New Name".',
                tools_used=tools_used,
            )
        new_name_match = re.search(r"(?:to|rename to|new name)\s+[\"']?([a-zA-Z0-9 \-_]+)[\"']?$", prompt.strip(), flags=re.IGNORECASE)
        desc_match = re.search(r"description\s*[:\s]+(.+?)(?:\.|$)", prompt, flags=re.IGNORECASE)
        cat_match = re.search(r"category\s*[:\s]+([a-zA-Z0-9 \-_]+?)(?:\s|$)", prompt, flags=re.IGNORECASE)
        tools_used.append("update_recipe")
        factual = await mcp_client.call_tool(
            "update_recipe",
            {
                "recipe_name": recipe,
                "user_id": user_id,
                **({"new_name": new_name_match.group(1).strip()} if new_name_match else {}),
                **({"description": desc_match.group(1).strip()} if desc_match else {}),
                **({"category": cat_match.group(1).strip()} if cat_match else {}),
            },
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # create recipe
    if re.search(r"\b(create|add|new)\b.{0,20}\brecipe\b", normalized):
        recipe = _extract_recipe_name(prompt)
        if not recipe:
            return AgentResult(
                reply=(
                    'Please specify the recipe name. For a full recipe with ingredients use:\n'
                    '"create recipe \\"Pasta\\" with ingredients: flour 200 g, water 100 ml"'
                ),
                tools_used=tools_used,
            )
        # Parse inline ingredients: name amount unit pairs
        ing_matches = re.findall(
            r"([a-zA-Z][a-zA-Z0-9 \-_]*?)\s+(\d+(?:\.\d+)?)\s*(g|kg|ml|L|tsp|tbsp|cup|oz|lb|unit)",
            prompt,
            flags=re.IGNORECASE,
        )
        ingredients = [{"name": m[0].strip(), "amount": float(m[1]), "unit": m[2]} for m in ing_matches]
        desc_match = re.search(r"description\s*[:\s]+(.+?)(?:,|with ingredients|\.|$)", prompt, flags=re.IGNORECASE)
        yield_match = re.search(
            r"(?:yields?|makes?|for)\s+(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?",
            prompt,
            flags=re.IGNORECASE,
        )
        yield_amount = float(yield_match.group(1)) if yield_match else 1
        yield_unit = (yield_match.group(2) or "portion").strip() if yield_match else "portion"
        tools_used.append("create_full_recipe")
        factual = await mcp_client.call_tool(
            "create_full_recipe",
            {
                "name": recipe,
                "description": desc_match.group(1).strip() if desc_match else "",
                "ingredients": ingredients,
                "yield_amount": yield_amount,
                "yield_unit": yield_unit,
                "user_id": user_id,
            },
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # add ingredient to recipe
    if re.search(r"\badd\b.{0,30}\bto\b.{0,30}\brecipe\b", normalized) or \
       re.search(r"\badd ingredient.{0,30}(to|into)\b", normalized):
        recipe = _extract_recipe_name(prompt)
        ing_match = re.search(r"add\s+([a-zA-Z][a-zA-Z0-9 \-_]*?)\s+(\d+(?:\.\d+)?)\s*(g|kg|ml|L|tsp|tbsp|cup|oz|lb|unit)?", prompt, flags=re.IGNORECASE)
        if not recipe or not ing_match:
            return AgentResult(
                reply='Please specify ingredient and recipe, e.g. add Flour 200 g to recipe "Bread".',
                tools_used=tools_used,
            )
        tools_used.append("add_ingredient_to_recipe")
        factual = await mcp_client.call_tool(
            "add_ingredient_to_recipe",
            {
                "recipe_name": recipe,
                "ingredient_name": ing_match.group(1).strip(),
                "amount": float(ing_match.group(2)),
                "unit": ing_match.group(3) or "unit",
                "user_id": user_id,
            },
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # update ingredient quantity in a recipe
    if re.search(r"\b(update|change|set)\b.{0,30}\bquantity\b", normalized) or \
       re.search(r"\bquantity\b.{0,30}\b(update|change|set)\b", normalized):
        recipe = _extract_recipe_name(prompt)
        ing_name_match = re.search(r"(?:of\s+)?([a-zA-Z][a-zA-Z0-9 \-_]+?)\s+(?:quantity|amount|to\s+\d)", prompt, flags=re.IGNORECASE)
        new_amount = _extract_amount(prompt)
        if not recipe or not ing_name_match or new_amount is None:
            return AgentResult(
                reply='Please specify recipe, ingredient, and new amount, e.g. update quantity of Flour to 300 in recipe "Bread".',
                tools_used=tools_used,
            )
        tools_used.append("update_recipe_ingredient_quantity")
        factual = await mcp_client.call_tool(
            "update_recipe_ingredient_quantity",
            {
                "recipe_name": recipe,
                "ingredient_name": ing_name_match.group(1).strip(),
                "new_amount": new_amount,
                "user_id": user_id,
            },
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # remove ingredient from recipe
    if re.search(r"\b(remove|delete)\b.{0,30}\bfrom\b.{0,30}\brecipe\b", normalized) or \
       re.search(r"\bremove ingredient\b", normalized):
        recipe = _extract_recipe_name(prompt)
        from_match = re.search(r"(?:remove|delete)\s+([a-zA-Z][a-zA-Z0-9 \-_]+?)\s+from", prompt, flags=re.IGNORECASE)
        if not recipe or not from_match:
            return AgentResult(
                reply='Please specify ingredient and recipe, e.g. remove Flour from recipe "Bread".',
                tools_used=tools_used,
            )
        tools_used.append("remove_ingredient_from_recipe")
        factual = await mcp_client.call_tool(
            "remove_ingredient_from_recipe",
            {
                "recipe_name": recipe,
                "ingredient_name": from_match.group(1).strip(),
                "user_id": user_id,
            },
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    # --- Read operations ---

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

    if "scale" in normalized or re.search(r"\b(for|make|want|need)\b.{0,15}\b\d+\b", normalized):
        # Extract target amount + optional unit: "4 portions", "250 g", "6 cookies", "2 loaves"
        target_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(portions?|servings?|g|kg|ml|L|oz|lb|cookies?|loaves?|loaf|pieces?|units?)?",
            prompt,
            flags=re.IGNORECASE,
        )
        recipe = _extract_recipe_name(prompt)
        if not recipe or not target_match:
            return AgentResult(
                reply='Please specify recipe and desired amount, e.g. scale "Hummus" to 250 g or scale "Pasta" for 2 portions.',
                tools_used=tools_used,
            )
        target_amount = float(target_match.group(1))
        target_unit = (target_match.group(2) or "").strip()
        tools_used.append("scale_recipe")
        factual = await mcp_client.call_tool(
            "scale_recipe",
            {"recipe_name": recipe, "target_amount": target_amount, "target_unit": target_unit, "user_id": user_id},
        )
        return AgentResult(reply=await llm_client.format_kitchen_response(prompt, factual), tools_used=tools_used)

    if "substitut" in normalized:
        ingredient = _extract_substitution_ingredient(prompt)
        if not ingredient:
            return AgentResult(
                reply="Tell me which ingredient you need to replace, e.g. substitution for egg.",
                tools_used=tools_used,
            )

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
    reply = await llm_client.answer_general_kitchen_question(prompt, fallback)
    return AgentResult(reply=reply, tools_used=tools_used)
