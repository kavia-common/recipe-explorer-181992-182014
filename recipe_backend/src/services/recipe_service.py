"""
Service layer for recipe operations.

This module encapsulates business logic for listing, retrieving, and creating recipes.
It depends on the Repository abstraction which is injected by the API layer.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from src.db.repository import Repository
from src.models.recipe import Recipe, RecipeCreate
from src.schemas.common import RecipeListQuery


class RecipeService:
    """Service class orchestrating recipe-related operations."""

    def __init__(self, repository: Repository) -> None:
        self.repo = repository

    # PUBLIC_INTERFACE
    def list_recipes(self, params: RecipeListQuery) -> dict:
        """
        List recipes using repository with search/filter/pagination.

        Returns a dict with keys:
        - items: List[Recipe]
        - total: int
        """
        result = self.repo.list_recipes(
            q=params.q,
            category=params.category,
            tags=params.tags,
            page=params.page,
            page_size=params.page_size,
        )
        # Ensure keys exist
        return {"items": result.get("items", []), "total": int(result.get("total", 0))}

    # PUBLIC_INTERFACE
    def get_recipe(self, recipe_id: str) -> Recipe:
        """Return a single recipe or raise 404 if not found."""
        recipe = self.repo.get_recipe(recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recipe with id '{recipe_id}' not found",
            )
        return recipe

    # PUBLIC_INTERFACE
    def create_recipe(self, payload: RecipeCreate) -> Recipe:
        """Create a new recipe via repository and return it."""
        return self.repo.create_recipe(payload)
