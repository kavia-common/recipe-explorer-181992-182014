"""
Placeholder client for an external Recipe Database service.

This client would be responsible for communicating with an external
service using the configured URL and API key. For now, it only defines
stubs to satisfy the adapter pattern used by ExternalRepository.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class RecipeDatabaseClient:
    """Client for external recipe database service."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def _headers(self) -> Dict[str, str]:
        """Return auth headers for API calls."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"
        return headers

    # Below methods are stubs that should be implemented when integrating
    # with a real service. They currently raise NotImplementedError.

    def list_recipes(
        self,
        q: Optional[str],
        category: Optional[str],
        tags: Optional[List[str]],
        page: int,
        page_size: int,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def get_recipe(self, recipe_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    def create_recipe(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
