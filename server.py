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


if __name__ == "__main__":
    mcp.run()
