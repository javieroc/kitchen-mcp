"""Supabase persistence for recipes and recipe ingredients."""

from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from supabase import Client

from .db import build_supabase_client

# Single select string reused for every recipe query so the shape is always consistent.
_RECIPE_SELECT = (
    "*, recipe_ingredients("
    "id, recipe_id, ingredient_id, quantity_used, created_at, "
    "ingredients(name, unit_of_measure, cost_per_unit)"
    ")"
)


class RecipeStore:
    """Data access layer for recipe entities."""

    def __init__(self, access_token: str) -> None:
        self.client: Client = build_supabase_client(access_token)

    # ------------------------------------------------------------------
    # Recipes — single-query loading via PostgREST embedding
    # ------------------------------------------------------------------

    def list_recipes(self, user_id: str) -> list[dict[str, Any]]:
        """Return all recipes with their ingredients in one query."""
        response = (
            self.client.table("recipes")
            .select(_RECIPE_SELECT)
            .eq("owner_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data or []

    def list_recipes_page(
        self,
        user_id: str,
        limit: int,
        before: str | None = None,
    ) -> tuple[list[dict[str, Any]], bool]:
        """Return a page of recipes (newest first) and whether older ones exist.

        Fetches ``limit + 1`` rows to detect ``has_more`` without a count query.

        Args:
            before: Exclusive upper bound on ``created_at`` (ISO string cursor).
                    When supplied, only recipes older than this cursor are returned.

        Returns:
            A tuple of (recipes newest-first, has_more).
        """
        query = (
            self.client.table("recipes")
            .select(_RECIPE_SELECT)
            .eq("owner_id", user_id)
            .order("created_at", desc=True)
            .limit(limit + 1)
        )
        if before is not None:
            query = query.lt("created_at", before)

        rows = query.execute().data or []

        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]

        return rows, has_more

    def get_recipe(self, recipe_id: UUID, user_id: str) -> dict[str, Any] | None:
        """Return a single recipe with its ingredients in one query."""
        response = (
            self.client.table("recipes")
            .select(_RECIPE_SELECT)
            .eq("id", str(recipe_id))
            .eq("owner_id", user_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return rows[0] if rows else None

    def create_recipe(
        self,
        user_id: str,
        name: str,
        description: str | None = None,
        category: str | None = None,
        image_url: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"owner_id": user_id, "name": name.strip()}
        if description is not None:
            payload["description"] = description.strip()
        if category is not None:
            payload["category"] = category.strip()
        if image_url is not None:
            payload["image_url"] = image_url.strip()
        response = self.client.table("recipes").insert(payload).execute()
        if not response.data:
            raise RuntimeError("Could not create recipe.")
        return response.data[0]

    def create_recipe_with_ingredients(
        self,
        user_id: str,
        name: str,
        description: str | None,
        ingredients: list[dict[str, Any]],  # [{"ingredient_id": str, "quantity_used": float}]
        category: str | None = None,
        image_url: str | None = None,
    ) -> dict[str, Any]:
        """Insert the recipe row, batch-insert all links, return full embedded row."""
        recipe_row = self.create_recipe(
            user_id=user_id,
            name=name,
            description=description,
            category=category,
            image_url=image_url,
        )
        recipe_id = recipe_row["id"]

        if ingredients:
            links = [
                {
                    "recipe_id": recipe_id,
                    "ingredient_id": item["ingredient_id"],
                    "quantity_used": item["quantity_used"],
                    "owner_id": user_id,
                }
                for item in ingredients
            ]
            self.client.table("recipe_ingredients").insert(links).execute()

        # Re-fetch with embedding so the caller always gets a consistent shape.
        row = self.get_recipe(UUID(recipe_id), user_id)
        if not row:
            raise RuntimeError("Could not retrieve newly created recipe.")
        return row

    def update_recipe(
        self,
        recipe_id: UUID,
        user_id: str,
        name: str | None = None,
        description: str | None = None,
        category: str | None = None,
        image_url: str | None = None,
    ) -> dict[str, Any] | None:
        patch: dict[str, Any] = {}
        if name is not None:
            patch["name"] = name.strip()
        if description is not None:
            patch["description"] = description.strip()
        if category is not None:
            patch["category"] = category.strip()
        if image_url is not None:
            patch["image_url"] = image_url.strip()
        if not patch:
            return self.get_recipe(recipe_id, user_id)

        response = (
            self.client.table("recipes")
            .update(patch)
            .eq("id", str(recipe_id))
            .eq("owner_id", user_id)
            .execute()
        )
        if not (response.data or []):
            return None
        return self.get_recipe(recipe_id, user_id)

    def delete_recipe(self, recipe_id: UUID, user_id: str) -> bool:
        response = (
            self.client.table("recipes")
            .delete()
            .eq("id", str(recipe_id))
            .eq("owner_id", user_id)
            .execute()
        )
        return bool(response.data)

    # ------------------------------------------------------------------
    # Ingredients — get-or-create
    # ------------------------------------------------------------------

    def get_or_create_ingredient(
        self,
        name: str,
        user_id: str,
        unit_of_measure: str = "unit",
        cost_per_unit: Decimal = Decimal("0.00"),
    ) -> dict[str, Any]:
        """Return the existing ingredient row or create and return a new one."""
        response = (
            self.client.table("ingredients")
            .select("id, name, unit_of_measure, cost_per_unit")
            .eq("name", name.strip())
            .eq("owner_id", user_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if rows:
            return rows[0]

        insert_response = (
            self.client.table("ingredients")
            .insert({
                "name": name.strip(),
                "unit_of_measure": unit_of_measure,
                "cost_per_unit": float(cost_per_unit),
                "owner_id": user_id,
            })
            .execute()
        )
        if not insert_response.data:
            raise RuntimeError(f"Could not create ingredient '{name}'.")
        return insert_response.data[0]

    # ------------------------------------------------------------------
    # Recipe ingredient links
    # ------------------------------------------------------------------

    def add_recipe_ingredient(
        self,
        recipe_id: UUID,
        ingredient_id: UUID,
        quantity_used: Decimal,
        user_id: str,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "recipe_id": str(recipe_id),
            "ingredient_id": str(ingredient_id),
            "quantity_used": float(quantity_used),
            "owner_id": user_id,
        }
        response = self.client.table("recipe_ingredients").insert(payload).execute()
        if not response.data:
            raise RuntimeError("Could not add ingredient to recipe.")
        return response.data[0]

    def update_recipe_ingredient(
        self,
        recipe_id: UUID,
        ingredient_id: UUID,
        quantity_used: Decimal,
        user_id: str,
    ) -> bool:
        response = (
            self.client.table("recipe_ingredients")
            .update({"quantity_used": float(quantity_used)})
            .eq("recipe_id", str(recipe_id))
            .eq("ingredient_id", str(ingredient_id))
            .eq("owner_id", user_id)
            .execute()
        )
        return bool(response.data)

    def remove_recipe_ingredient(
        self, recipe_id: UUID, ingredient_id: UUID, user_id: str
    ) -> bool:
        response = (
            self.client.table("recipe_ingredients")
            .delete()
            .eq("recipe_id", str(recipe_id))
            .eq("ingredient_id", str(ingredient_id))
            .eq("owner_id", user_id)
            .execute()
        )
        return bool(response.data)
