# Recipe Backend

Environment variables:
- RECIPE_DB_PROVIDER: "memory" | "external" (default "memory")
- RECIPE_DB_URL: external service base URL (when provider="external")
- RECIPE_DB_API_KEY: API key for external service
- ALLOW_ORIGINS: comma-separated origins for CORS (default "http://localhost:3000")

Run:
- uvicorn src.api.main:app --reload --port 3001

CORS:
Ensure ALLOW_ORIGINS includes your frontend origin (e.g., http://localhost:3000).
