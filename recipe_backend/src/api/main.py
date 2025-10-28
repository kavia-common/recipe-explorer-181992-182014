from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.db.repository import InMemoryRepository, ExternalRepository, Repository
from src.db.clients.recipe_database_client import RecipeDatabaseClient
from src.api.routers.recipes import router as recipes_router


settings = get_settings()

# Initialize FastAPI with OpenAPI metadata and tags
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    openapi_tags=[
        {"name": "health", "description": "Service health and status"},
        {"name": "recipes", "description": "Recipe browsing and management"},
    ],
)

# CORS - permissive for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_repository() -> Repository:
    """
    Factory to build a repository instance based on environment configuration.
    Defaults to the in-memory repository.
    """
    provider = settings.RECIPE_DB_PROVIDER
    if provider == "external":
        client = RecipeDatabaseClient(
            base_url=settings.RECIPE_DB_URL,
            api_key=settings.RECIPE_DB_API_KEY,
        )
        # External repository is currently a stub with NotImplemented methods.
        # Keeping construction here to validate dependency chain and allow
        # future implementation without changing DI wiring.
        return ExternalRepository(client)
    # Default
    return InMemoryRepository()


# PUBLIC_INTERFACE
def get_repository() -> Generator[Repository, None, None]:
    """Dependency provider yielding a repository instance for request handling."""
    repo = _build_repository()
    try:
        yield repo
    finally:
        # No cleanup needed for in-memory; placeholder for external client cleanup.
        pass


@app.get(
    "/",
    tags=["health"],
    summary="Health Check",
    description="Returns a simple payload to indicate the service is running.",
)
def health_check():
    """Health check endpoint returning service status information."""
    return {"message": "Healthy", "provider": settings.RECIPE_DB_PROVIDER}


# Register routers
app.include_router(recipes_router)
