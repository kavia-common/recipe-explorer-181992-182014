"""
Common Pydantic schemas for query parameters and pagination.

These models are used across multiple endpoints to ensure consistent
validation and documentation in the OpenAPI schema.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class PaginationParams(BaseModel):
    """Pagination query parameters with validation and sensible defaults."""
    page: int = Field(1, ge=1, description="Page number starting at 1")
    page_size: int = Field(10, ge=1, le=100, description="Number of items per page (1-100)")


class RecipeListQuery(PaginationParams):
    """Query parameters for listing recipes with optional search and filters."""
    q: Optional[str] = Field(None, description="Free-text search across title, description and tags")
    category: Optional[str] = Field(None, description="Filter by recipe category, e.g., 'Dessert'")
    tags: Optional[List[str]] = Field(
        default=None,
        description="Filter by tags; all provided tags must be present on a recipe",
    )

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v):
        """
        Accept both repeated query params (?tags=a&tags=b) and a single comma-separated string (?tags=a,b).
        """
        if v is None:
            return None
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        # Handle comma-separated
        return [s.strip() for s in str(v).split(",") if s.strip()]


class PaginatedResponse(BaseModel):
    """Generic pagination envelope used by some list endpoints."""
    total: int = Field(..., description="Total number of items across all pages")
