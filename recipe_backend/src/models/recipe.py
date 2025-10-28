"""
Pydantic models representing the Recipe domain.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    """Represents a single ingredient with quantity and unit."""
    name: str = Field(..., description="Name of the ingredient, e.g., 'Flour'")
    quantity: Optional[float] = Field(None, description="Numeric measurement amount")
    unit: Optional[str] = Field(None, description="Measurement unit, e.g., 'g', 'cups'")


class Step(BaseModel):
    """Represents a single step in a recipe."""
    order: int = Field(..., description="Step order starting at 1")
    instruction: str = Field(..., description="Text instruction for the step")


class RecipeBase(BaseModel):
    """Base fields common to create and read models."""
    title: str = Field(..., description="Recipe title")
    description: Optional[str] = Field(None, description="Short description of the recipe")
    category: Optional[str] = Field(None, description="Recipe category, e.g., 'Dessert'")
    tags: List[str] = Field(default_factory=list, description="List of tags")
    ingredients: List[Ingredient] = Field(default_factory=list, description="List of ingredients")
    steps: List[Step] = Field(default_factory=list, description="Ordered list of steps")
    image_url: Optional[str] = Field(None, description="Optional image URL for the recipe")


class RecipeCreate(RecipeBase):
    """Model used for creating a recipe."""
    pass


class Recipe(RecipeBase):
    """Model representing a persisted recipe with an ID."""
    id: str = Field(..., description="Unique ID of the recipe")
