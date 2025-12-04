"""
Importer script: loads `data/recipes.json` and inserts into backend SQLite DB.
Usage:
  python import_recipes.py
"""

import os
import json
from app import app
from models import db, Recipe

# JSON dosyasının yolu
DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "recipes.json"
)

with app.app_context():
    # JSON oku
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Her tarifi veritabanına ekle
    for item in data:
        if Recipe.query.get(item["id"]):
            print("Skipping existing", item["id"])
            continue

        r = Recipe(
            id=item["id"],
            title=item.get("title"),
            category=item.get("category"),
            excerpt=item.get("excerpt"),
            image=item.get("image"),
            url=item.get("url"),
            prep=item.get("prep"),
            cook=item.get("cook"),
            servings=item.get("servings"),
            ingredients=json.dumps(item.get("ingredients", [])),
            steps=json.dumps(item.get("steps", [])),
            tags=json.dumps(item.get("tags", [])),
        )

        db.session.add(r)

    db.session.commit()
    print("Import complete")
