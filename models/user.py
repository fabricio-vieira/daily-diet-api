from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True )
    email = db.Column(db.String(80), nullable=False)
    meals =db.relationship('Meal', backref='user', lazy=True)