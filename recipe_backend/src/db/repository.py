"""
Repository abstraction for the Recipe domain.

Includes:
- Repository protocol/interface definition
- InMemoryRepository: simple in-memory implementation with seed data
- ExternalRepository: adapter wrapper around an external client (stubbed)
"""

from __future__ import annotations

import itertools
from typing import Dict, List, Optional, Tuple, TypedDict

from src.models.recipe import Recipe, RecipeCreate
from src.db.clients.recipe_database_client import RecipeDatabaseClient


class PaginatedRecipes(TypedDict):
    """Typed dict response for paginated recipe list."""
    items: List[Recipe]
    total: int


class Repository:
    """Repository interface for recipe data operations."""

    # PUBLIC_INTERFACE
    def list_recipes(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedRecipes:
        """List recipes with optional search, filtering, and pagination."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """Retrieve a single recipe by id."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def create_recipe(self, data: RecipeCreate) -> Recipe:
        """Create and return a new recipe."""
        raise NotImplementedError


class InMemoryRepository(Repository):
    """Simple in-memory repository suitable for development and tests."""

    def __init__(self) -> None:
        self._recipes: Dict[str, Recipe] = {}
        self._id_counter = itertools.count(1)
        self._seed()

    def _seed(self) -> None:
        """Seed with some initial data for demo purposes."""
        sample_data: List[Tuple[str, str, str, List[str]]] = [
            ("Classic Pancakes", "Fluffy breakfast pancakes.", "Breakfast", ["easy", "quick"]),
            ("Spaghetti Carbonara", "Creamy pasta with pancetta.", "Dinner", ["italian", "comfort"]),
            ("Avocado Toast", "Simple and healthy toast.", "Breakfast", ["healthy", "quick"]),
            ("Chocolate Brownies", "Rich and fudgy brownies.", "Dessert", ["chocolate", "baking"]),
        ]
        for title, desc, category, tags in sample_data:
            rid = str(next(self._id_counter))
            recipe = Recipe(
                id=rid,
                title=title,
                description=desc,
                category=category,
                tags=tags,
                ingredients=[],
                steps=[],
                image_url=None,
            )
            self._recipes[rid] = recipe

    def list_recipes(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedRecipes:
        items = list(self._recipes.values())

        # Filter by search query
        if q:
            q_lower = q.lower()
            items = [
                r for r in items
                if q_lower in r.title.lower()
                or (r.description and q_lower in r.description.lower())
                or any(q_lower in t.lower() for t in r.tags)
            ]

        # Filter by category
        if category:
            items = [r for r in items if (r.category or "").lower() == category.lower()]

        # Filter by tags (all provided tags must be present)
        if tags:
            tag_set = {t.lower() for t in tags}
            items = [r for r in items if tag_set.issubset({t.lower() for t in r.tags})]

        total = len(items)

        # Pagination bounds
        page = max(1, page)
        page_size = max(1, min(page_size, 100))
        start = (page - 1) * page_size
        end = start + page_size
        paged_items = items[start:end]

        return {"items": paged_items, "total": total}

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        return self._recipes.get(recipe_id)

    def create_recipe(self, data: RecipeCreate) -> Recipe:
        rid = str(next(self._id_counter))
        recipe = Recipe(id=rid, **data.model_dump())
        self._recipes[rid] = recipe
        return recipe


class ExternalRepository(Repository):
    """
    Adapter repository for an external database or API.

    This wraps RecipeDatabaseClient to perform CRUD operations.
    For now, methods are stubbed with NotImplementedError to indicate
    where integration should occur.
    """

    def __init__(self, client: RecipeDatabaseClient) -> None:
        self.client = client

    def list_recipes(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedRecipes:
        # Placeholder implementation: raise until integrated
        raise NotImplementedError("ExternalRepository.list_recipes is not implemented yet.")

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        # Placeholder implementation: raise until integrated
        raise NotImplementedError("ExternalRepository.get_recipe is not implemented yet.")

    def create_recipe(self, data: RecipeCreate) -> Recipe:
        # Placeholder implementation: raise until integrated
        raise NotImplementedError("ExternalRepository.create_recipe is not implemented yet.")
