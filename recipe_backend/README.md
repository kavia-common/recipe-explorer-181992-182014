# Recipe Backend

Environment variables:
- RECIPE_DB_PROVIDER: "memory" | "external" (default "memory")
- RECIPE_DB_URL: external service base URL (when provider="external")
- RECIPE_DB_API_KEY: API key for external service
- ALLOW_ORIGINS: comma-separated origins for CORS (default "http://localhost:3000")

Defaults:
- Provider defaults to in-memory. No external DB is required for local development.
- CORS allows http://localhost:3000 by default for the React dev server.

Run:
- uvicorn src.api.main:app --reload --port 3001

OpenAPI:
- To regenerate the OpenAPI spec after changing API or models, run:
  python -m src.api.generate_openapi
  The schema will be written to interfaces/openapi.json.

CORS:
Ensure ALLOW_ORIGINS includes your frontend origin (e.g., http://localhost:3000).
