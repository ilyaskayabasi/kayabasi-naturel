import os
import json
from flask import Flask, jsonify, request, abort
from dotenv import load_dotenv
from flask_cors import CORS
from models import db, Recipe

load_dotenv()

DB_PATH = os.getenv('DATABASE_URL', 'sqlite:///recipes.db')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'devtoken')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Render uyumlu: veritabanını burada oluşturuyoruz
with app.app_context():
    db.create_all()

CORS(app, resources={r"/api/*": {"origins": "*"}})


# Helper: require admin token in header X-Admin-Token for write operations
def require_admin():
    token = request.headers.get('X-Admin-Token', '')
    if token != ADMIN_TOKEN:
        abort(401, description='Unauthorized')


# API: list recipes
@app.route('/api/recipes', methods=['GET'])
def list_recipes():
    r = Recipe.query.all()
    return jsonify([item.to_dict() for item in r])


# API: get single recipe
@app.route('/api/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    r = Recipe.query.get_or_404(recipe_id)
    return jsonify(r.to_dict())


# API: create recipe
@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    require_admin()
    data = request.get_json() or {}

    if 'id' not in data or 'title' not in data:
        abort(400, 'id and title are required')

    if Recipe.query.get(data['id']):
        abort(409, 'Recipe with this id already exists')

    import json as _json

    r = Recipe(
        id=data['id'],
        title=data.get('title'),
        category=data.get('category'),
        excerpt=data.get('excerpt'),
        image=data.get('image'),
        url=data.get('url'),
        prep=data.get('prep'),
        cook=data.get('cook'),
        servings=data.get('servings'),
        ingredients=_json.dumps(data.get('ingredients', [])),
        steps=_json.dumps(data.get('steps', [])),
        tags=_json.dumps(data.get('tags', []))
    )

    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201


# API: update
@app.route('/api/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    require_admin()
    r = Recipe.query.get_or_404(recipe_id)
    data = request.get_json() or {}

    for key in ('title', 'category', 'excerpt', 'image', 'url', 'prep', 'cook', 'servings'):
        if key in data:
            setattr(r, key, data[key])

    import json as _json

    if 'ingredients' in data:
        r.ingredients = _json.dumps(data['ingredients'])
    if 'steps' in data:
        r.steps = _json.dumps(data['steps'])
    if 'tags' in data:
        r.tags = _json.dumps(data['tags'])

    db.session.commit()
    return jsonify(r.to_dict())


# API: delete
@app.route('/api/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    require_admin()
    r = Recipe.query.get_or_404(recipe_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'deleted': recipe_id})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(os.getenv('PORT', 5000)))



















# --- ADMIN IMPORT ENDPOINT ---
import json
from models import Recipe, db

@app.route('/admin/import', methods=['POST'])
def admin_import():
    token = request.headers.get("X-Admin-Token")
    if token != os.getenv("ADMIN_TOKEN"):
        return {"error": "unauthorized"}, 401

    DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

    if not os.path.exists(DATA_FILE):
        return {"error": "recipes.json not found"}, 404

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    added = 0
    skipped = 0

    for item in data:
        if Recipe.query.get(item['id']):
            skipped += 1
            continue

        r = Recipe(
            id=item['id'],
            title=item.get('title'),
            category=item.get('category'),
            excerpt=item.get('excerpt'),
            image=item.get('image'),
            url=item.get('url'),
            prep=item.get('prep'),
            cook=item.get('cook'),
            servings=item.get('servings'),
            ingredients=json.dumps(item.get('ingredients', [])),
            steps=json.dumps(item.get('steps', [])),
            tags=json.dumps(item.get('tags', [])),
        )
        db.session.add(r)
        added += 1

    db.session.commit()

    return {
        "status": "import complete",
        "added": added,
        "skipped": skipped
    }
