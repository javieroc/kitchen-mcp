import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

mcp = FastMCP("Kitchen_Orchestrator")

@mcp.tool()
def check_connection() -> str:
    """Verifies that the MCP server can talk to the Supabase database."""
    try:
        supabase.table("ingredients").select("id", count="exact").limit(1).execute()
        return "Connection to Supabase is active and healthy."
    except Exception as e:
        return f"Connection failed: {str(e)}"


@mcp.tool()
def add_ingredient(name: str, unit: str, cost: float) -> str:
    """
    Adds a new ingredient to the kitchen catalog.

    Args:
        name: Unique name of the ingredient (e.g., 'Extra Virgin Olive Oil').
        unit: Unit of measure (must be one of the SQL Enum types: g, kg, ml, L, unit, etc.).
        cost: The cost per that specific unit (e.g., 0.05).
    """
    try:
        ingredient_data = {
            "name": name,
            "unit_of_measure": unit,
            "cost_per_unit": cost
        }

        response = supabase.table("ingredients").insert(ingredient_data).execute()

        return f"Successfully added {name} at ${cost} per {unit} to the catalog."

    except Exception as e:
        return f"Error adding ingredient: {str(e)}"


@mcp.tool()
def update_ingredient_price(name: str, new_cost: float) -> str:
    """
    Updates the cost of an existing ingredient.
    All recipes using this ingredient will reflect the new price immediately.
    """
    try:
        supabase.table("ingredients").update({"cost_per_unit": new_cost}).eq("name", name).execute()
        return f"Updated {name} cost to ${new_cost}."
    except Exception as e:
        return f"Error updating price: {str(e)}"


@mcp.tool()
def list_available_recipes() -> str:
    """
    Returns a list of all recipe names and descriptions in the database.
    """
    try:
        res = supabase.table("recipes").select("name, description").execute()
        if not res.data:
            return "No recipes found in the database."

        output = "**Available Recipes:**\n"
        for r in res.data:
            desc = r['description'] if r['description'] else "No description"
            output += f"- **{r['name']}**: {desc}\n"
        return output
    except Exception as e:
        return f"Error listing recipes: {str(e)}"


@mcp.tool()
def create_full_recipe(name: str, description: str, ingredients: list[dict]) -> str:
    """
    Creates a new recipe and links multiple ingredients to it.

    Args:
        name: Name of the dish (e.g., 'Margherita Pizza').
        description: A brief description.
        ingredients: A list of objects with 'name' and 'amount'.
                     Example: [{"name": "00 Flour", "amount": 250}, {"name": "Water", "amount": 165}]
    """
    try:
        recipe_res = supabase.table("recipes").insert({
            "name": name,
            "description": description
        }).execute()
        recipe_id = recipe_res.data[0]['id']

        links_created = 0

        for item in ingredients:
            ing_name = item['name']
            amount = item['amount']

            ing_res = supabase.table("ingredients").select("id").eq("name", ing_name).single().execute()

            if ing_res.data:
                supabase.table("recipe_ingredients").insert({
                    "recipe_id": recipe_id,
                    "ingredient_id": ing_res.data['id'],
                    "quantity_used": amount
                }).execute()
                links_created += 1

        return f"Successfully created '{name}' with {links_created} ingredients linked."

    except Exception as e:
        return f"Error creating recipe: {str(e)}"


@mcp.tool()
def get_recipe_ingredients(recipe_name: str) -> str:
    """
    Lists all ingredients and their quantities for a specific recipe.
    """
    try:
        res = supabase.table("recipe_ingredients") \
            .select("quantity_used, ingredients(name, unit_of_measure), recipes!inner(name)") \
            .eq("recipes.name", recipe_name) \
            .execute()

        if not res.data:
            return f"No ingredients found for '{recipe_name}'."

        output = f"**Ingredients for {recipe_name}:**\n"
        for item in res.data:
            ing = item['ingredients']
            output += f"- {ing['name']}: {item['quantity_used']} {ing['unit_of_measure']}\n"
        return output
    except Exception as e:
        return f"Error fetching details: {str(e)}"


@mcp.tool()
def scale_recipe(recipe_name: str, servings: int) -> str:
    """
    Calculates the total weight and cost of ingredients needed for multiple servings.
    """
    try:
        res = supabase.table("recipe_ingredients") \
            .select("""
                quantity_used,
                recipes!inner(name),
                ingredients(name, unit_of_measure, cost_per_unit)
            """) \
            .eq("recipes.name", recipe_name) \
            .execute()

        if not res.data:
            return f"Recipe '{recipe_name}' not found or has no ingredients."

        output = f"**Production Plan for {servings}x {recipe_name}**\n"
        grand_total = 0

        for item in res.data:
            ing = item['ingredients']
            qty_per_serving = item['quantity_used']

            total_qty = qty_per_serving * servings
            total_cost = total_qty * ing['cost_per_unit']
            grand_total += total_cost

            output += (f"- {ing['name']}: {total_qty}{ing['unit_of_measure']} "
                       f"(Cost: ${total_cost:.2f})\n")

        output += f"---\n**Total Batch Cost: ${grand_total:.2f}**"
        return output

    except Exception as e:
        return f"Error scaling recipe: {str(e)}"


@mcp.tool()
def calculate_recipe_cost(recipe_name: str) -> str:
    """
    Calculates the total production cost of a recipe by joining the
    recipe_ingredients, recipes, and ingredients tables.
    """
    try:
        res = supabase.table("recipe_ingredients") \
            .select("""
                quantity_used,
                recipes!inner(name),
                ingredients(name, cost_per_unit, unit_of_measure)
            """) \
            .eq("recipes.name", recipe_name) \
            .execute()

        if not res.data:
            return f"No ingredients found for recipe '{recipe_name}'."

        total_cost = 0.0
        breakdown = f"**Economic Breakdown for {recipe_name}**\n"
        breakdown += "------------------------------------------\n"

        for item in res.data:
            ing = item['ingredients']
            qty = float(item['quantity_used'])
            unit_cost = float(ing['cost_per_unit'])

            line_cost = qty * unit_cost
            total_cost += line_cost

            breakdown += (f"• {ing['name']}: {qty} {ing['unit_of_measure']} "
                          f"(@ ${unit_cost:.4f}) = **${line_cost:.2f}**\n")

        breakdown += "------------------------------------------\n"
        breakdown += f"**Total Recipe Cost: ${total_cost:.2f}**"

        return breakdown

    except Exception as e:
        return f"Error calculating cost: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
