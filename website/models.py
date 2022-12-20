from . import db
from flask_login import UserMixin

class Product(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    pictures = db.Column(db.String(500)) # Maybe to be created as own model with relationship to this one
    description = db.Column(db.String(5000))
    shipping_fee = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    products = db.relationship('Product')
