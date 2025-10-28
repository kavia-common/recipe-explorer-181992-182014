"""
Configuration module for the Recipe Backend.

Loads environment variables and exposes a strongly-typed settings object
used throughout the application to configure repository providers and CORS.

Environment variables:
- RECIPE_DB_PROVIDER: "memory" | "external" (default: "memory")
- RECIPE_DB_URL: URL for external recipe database API (default: "")
- RECIPE_DB_API_KEY: API key for external recipe database API (default: "")
- ALLOW_ORIGINS: Comma-separated list of allowed origins for CORS (default: "http://localhost:3000")
"""

from __future__ import annotations

import os
from typing import List


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        # Choose repository provider
        self.RECIPE_DB_PROVIDER: str = os.getenv("RECIPE_DB_PROVIDER", "memory").strip().lower()

        # External DB client configuration
        self.RECIPE_DB_URL: str = os.getenv("RECIPE_DB_URL", "").strip()
        self.RECIPE_DB_API_KEY: str = os.getenv("RECIPE_DB_API_KEY", "").strip()

        # CORS settings
        allow_origins_env = os.getenv("ALLOW_ORIGINS", "http://localhost:3000")
        self.ALLOW_ORIGINS: List[str] = [o.strip() for o in allow_origins_env.split(",") if o.strip()]

        # Basic app metadata
        self.APP_TITLE: str = os.getenv("APP_TITLE", "Recipe Explorer API")
        self.APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
        self.APP_DESCRIPTION: str = os.getenv(
            "APP_DESCRIPTION",
            "Backend API for a fullstack recipe application. Provides recipe browsing,"
            " search, and creation endpoints.",
        )


# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Return a singleton Settings instance."""
    # We avoid global state mutation; create per-call but could be cached if needed.
    return Settings()
