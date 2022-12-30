from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    pictures = db.Column(db.String(150))
    description = db.Column(db.String(5000))
    city = db.Column(db.String(150))
    category = db.Column(db.String(100))
    shipping_fee = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    products = db.relationship('Product')