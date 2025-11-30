Backend for Delicious recipe site (minimal Flask API)

Quick start (macOS / zsh):

1. Create virtualenv and install dependencies

```bash
cd /Users/doguhantaskin/Desktop/delicious-master/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Set admin token or DB URL

```bash
export ADMIN_TOKEN=your-secret-token
# You can also set DATABASE_URL to a different sqlite file or Postgres URL
# export DATABASE_URL=sqlite:///my.db
```

3. Import sample recipes (uses `../data/recipes.json`)

```bash
python import_recipes.py
```

4. Run dev server

```bash
python app.py
```

API endpoints
- GET `/api/recipes` — list all recipes
- GET `/api/recipes/<id>` — get single recipe
- POST `/api/recipes` — create (requires header `X-Admin-Token`)
- PUT `/api/recipes/<id>` — update (requires header `X-Admin-Token`)
- DELETE `/api/recipes/<id>` — delete (requires header `X-Admin-Token`)

Notes
- This is a minimal example to get a backend running quickly. For production you should:
  - Use a proper WSGI server (Gunicorn)
  - Use an actual database (Postgres)
  - Add proper authentication (login, sessions)
  - Add validation and error handling
