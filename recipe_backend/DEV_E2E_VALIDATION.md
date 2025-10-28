End-to-end validation checklist

Backend (FastAPI):
1) Install dependencies:
   pip install -r requirements.txt

2) Run backend on port 3001:
   uvicorn src.api.main:app --reload --port 3001

3) Optional: adjust env vars
   - RECIPE_DB_PROVIDER=memory (default)
   - ALLOW_ORIGINS=http://localhost:3000
   - If using external provider, set RECIPE_DB_URL and RECIPE_DB_API_KEY.

4) Regenerate OpenAPI after changes:
   python -m src.api.generate_openapi

Frontend (React):
1) From recipe_frontend, create .env if needed:
   REACT_APP_API_BASE_URL=http://localhost:3001
   (Defaults to http://localhost:3001 without .env)

2) Start dev server:
   npm install
   npm start

Manual flows:
- List: homepage should show seeded recipes from memory repo.
- Search: use search input and tags; backend supports q, category, tags (repeated or comma-separated), page, page_size.
- Detail: click a card to open detail modal; ingredients and steps render sorted by order.
- Create: click "+ Add Recipe", fill title and optional fields; after saving, the list refreshes (page resets to 1).

Troubleshooting:
- CORS errors: ensure backend ALLOW_ORIGINS includes frontend origin (http://localhost:3000).
- Network errors: verify REACT_APP_API_BASE_URL and backend port (3001).
- Schema mismatch: regenerate OpenAPI (python -m src.api.generate_openAPI) and confirm /interfaces/openapi.json updated.
