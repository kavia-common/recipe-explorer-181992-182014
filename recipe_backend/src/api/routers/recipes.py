from __future__ import annotations

from typing import Optional, List

from fastapi import APIRouter, Depends, status

from src.models.recipe import Recipe, RecipeCreate
from src.schemas.common import RecipeListQuery
from src.services.recipe_service import RecipeService
from src.api.main import get_repository  # provides Repository via Depends
from src.db.repository import Repository


router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=dict)
def list_recipes(
    q: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 10,
    repo: Repository = Depends(get_repository),
):
    """
    List recipes with optional search and pagination.

    Returns:
      { "items": Recipe[], "total": number }
    """
    # Build params via schema to reuse validation (including tags parsing)
    params = RecipeListQuery(q=q, category=category, tags=tags, page=page, page_size=page_size)
    service = RecipeService(repo)
    return service.list_recipes(params)


@router.get("/{recipe_id}", response_model=Recipe)
def get_recipe(
    recipe_id: str,
    repo: Repository = Depends(get_repository),
):
    """Get a single recipe by ID."""
    service = RecipeService(repo)
    return service.get_recipe(recipe_id)


@router.post("", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(
    payload: RecipeCreate,
    repo: Repository = Depends(get_repository),
):
    """Create a new recipe and return it."""
    service = RecipeService(repo)
    return service.create_recipe(payload)
