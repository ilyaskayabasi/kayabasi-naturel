from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.String(120), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(80), nullable=True)
    excerpt = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    prep = db.Column(db.String(80), nullable=True)
    cook = db.Column(db.String(80), nullable=True)
    servings = db.Column(db.String(80), nullable=True)
    ingredients = db.Column(db.Text, nullable=True)  # JSON string
    steps = db.Column(db.Text, nullable=True)        # JSON string
    tags = db.Column(db.Text, nullable=True)         # CSV or JSON

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'excerpt': self.excerpt,
            'image': self.image,
            'url': self.url,
            'prep': self.prep,
            'cook': self.cook,
            'servings': self.servings,
            'ingredients': json.loads(self.ingredients) if self.ingredients else [],
            'steps': json.loads(self.steps) if self.steps else [],
            'tags': json.loads(self.tags) if self.tags else []
        }
