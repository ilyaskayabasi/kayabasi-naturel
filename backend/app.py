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
CORS(app, resources={r"/api/*": {"origins": "*"}})

# NEW FIX — Flask 2.3 uyumlu tablo oluşturma
with app.app_context():
    db.create_all()

# Helper: require admin token
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
    for key in ('title','category','excerpt','image','url','prep','cook','servings'):
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
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
