"""Recipe CRUD endpoints."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import AuthenticatedUser, get_current_user
from ..models import (
    AddRecipeIngredientRequest,
    CreateRecipeRequest,
    Recipe,
    RecipeIngredientDetail,
    RecipeIngredientInput,
    RecipeWithIngredients,
    UpdateRecipeIngredientRequest,
    UpdateRecipeRequest,
)
from ..recipe_store import RecipeStore

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["recipes"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_store(user: AuthenticatedUser) -> RecipeStore:
    return RecipeStore(user.access_token)


def _to_recipe(row: dict) -> Recipe:
    return Recipe.model_validate(row)


def _to_ingredient_detail(row: dict) -> RecipeIngredientDetail:
    ingredient = row.get("ingredients") or {}
    return RecipeIngredientDetail(
        id=row["id"],
        recipe_id=row["recipe_id"],
        ingredient_id=row["ingredient_id"],
        quantity_used=row["quantity_used"],
        created_at=row["created_at"],
        ingredient_name=ingredient.get("name", ""),
        unit_of_measure=ingredient.get("unit_of_measure", ""),
        cost_per_unit=ingredient.get("cost_per_unit", 0),
    )


def _to_recipe_with_ingredients(row: dict) -> RecipeWithIngredients:
    return RecipeWithIngredients(
        recipe=_to_recipe(row),
        ingredients=[_to_ingredient_detail(r) for r in (row.get("recipe_ingredients") or [])],
    )


def _resolve_ingredients(
    store: RecipeStore,
    user_id: str,
    inputs: list[RecipeIngredientInput],
) -> list[dict]:
    """Get-or-create each ingredient and return link payloads."""
    resolved = []
    for item in inputs:
        ing = store.get_or_create_ingredient(
            name=item.name,
            user_id=user_id,
            unit_of_measure=item.unit_of_measure,
            cost_per_unit=item.cost_per_unit,
        )
        resolved.append({"ingredient_id": ing["id"], "quantity_used": float(item.quantity_used)})
    return resolved


# ---------------------------------------------------------------------------
# Recipe routes
# ---------------------------------------------------------------------------


@router.post("", response_model=RecipeWithIngredients, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    payload: CreateRecipeRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Create a recipe. Ingredients are looked up by name and auto-created if missing."""
    try:
        store = _get_store(user)
        resolved = _resolve_ingredients(store, user.user_id, payload.ingredients)
        row = store.create_recipe_with_ingredients(
            user_id=user.user_id,
            name=payload.name,
            description=payload.description,
            ingredients=resolved,
            category=payload.category,
            image_url=payload.image_url,
        )
        return _to_recipe_with_ingredients(row)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create recipe")
        raise HTTPException(status_code=500, detail="Failed to create recipe.") from exc


@router.get("", response_model=list[RecipeWithIngredients])
async def list_recipes(
    user: AuthenticatedUser = Depends(get_current_user),
):
    """List all recipes with their ingredients (single query)."""
    try:
        store = _get_store(user)
        rows = store.list_recipes(user_id=user.user_id)
        return [_to_recipe_with_ingredients(row) for row in rows]
    except Exception as exc:
        logger.exception("Failed to list recipes")
        raise HTTPException(status_code=500, detail="Failed to list recipes.") from exc


@router.get("/{recipe_id}", response_model=RecipeWithIngredients)
async def get_recipe(
    recipe_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Fetch a single recipe with its full ingredient list (single query)."""
    try:
        store = _get_store(user)
        row = store.get_recipe(recipe_id=recipe_id, user_id=user.user_id)
        if not row:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        return _to_recipe_with_ingredients(row)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to fetch recipe")
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.") from exc


@router.patch("/{recipe_id}", response_model=RecipeWithIngredients)
async def update_recipe(
    recipe_id: UUID,
    payload: UpdateRecipeRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Update a recipe's name and/or description."""
    try:
        store = _get_store(user)
        row = store.update_recipe(
            recipe_id=recipe_id,
            user_id=user.user_id,
            name=payload.name,
            description=payload.description,
            category=payload.category,
            image_url=payload.image_url,
        )
        if not row:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        return _to_recipe_with_ingredients(row)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update recipe")
        raise HTTPException(status_code=500, detail="Failed to update recipe.") from exc


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Delete a recipe and all its ingredient links."""
    try:
        store = _get_store(user)
        deleted = store.delete_recipe(recipe_id=recipe_id, user_id=user.user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Recipe not found.")
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete recipe")
        raise HTTPException(status_code=500, detail="Failed to delete recipe.") from exc


# ---------------------------------------------------------------------------
# Recipe ingredient routes
# ---------------------------------------------------------------------------


@router.post(
    "/{recipe_id}/ingredients",
    response_model=RecipeWithIngredients,
    status_code=status.HTTP_201_CREATED,
)
async def add_recipe_ingredient(
    recipe_id: UUID,
    payload: AddRecipeIngredientRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Add an ingredient to a recipe. Returns the updated recipe."""
    try:
        store = _get_store(user)
        if not store.get_recipe(recipe_id=recipe_id, user_id=user.user_id):
            raise HTTPException(status_code=404, detail="Recipe not found.")
        store.add_recipe_ingredient(
            recipe_id=recipe_id,
            ingredient_id=payload.ingredient_id,
            quantity_used=payload.quantity_used,
            user_id=user.user_id,
        )
        row = store.get_recipe(recipe_id=recipe_id, user_id=user.user_id)
        return _to_recipe_with_ingredients(row)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to add ingredient to recipe")
        raise HTTPException(status_code=500, detail="Failed to add ingredient.") from exc


@router.patch(
    "/{recipe_id}/ingredients/{ingredient_id}",
    response_model=RecipeWithIngredients,
)
async def update_recipe_ingredient(
    recipe_id: UUID,
    ingredient_id: UUID,
    payload: UpdateRecipeIngredientRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Update an ingredient quantity. Returns the updated recipe."""
    try:
        store = _get_store(user)
        updated = store.update_recipe_ingredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            quantity_used=payload.quantity_used,
            user_id=user.user_id,
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Recipe ingredient not found.")
        row = store.get_recipe(recipe_id=recipe_id, user_id=user.user_id)
        return _to_recipe_with_ingredients(row)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update recipe ingredient")
        raise HTTPException(status_code=500, detail="Failed to update ingredient.") from exc


@router.delete(
    "/{recipe_id}/ingredients/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_recipe_ingredient(
    recipe_id: UUID,
    ingredient_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Remove an ingredient from a recipe."""
    try:
        store = _get_store(user)
        deleted = store.remove_recipe_ingredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            user_id=user.user_id,
        )
        if not deleted:
            raise HTTPException(status_code=404, detail="Recipe ingredient not found.")
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to remove recipe ingredient")
        raise HTTPException(status_code=500, detail="Failed to remove ingredient.") from exc
