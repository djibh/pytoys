from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Product
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    get_all_products = db.session.query(Product).all()

    if request.method == 'POST':
        product_title = request.form.get('product-title')
        product_description = request.form.get('product-description')
        product_category = request.form.get('product-category')
        product_city = request.form.get('product-city')


        if len(product_title) < 1:
            flash('Product\'s description is too short!', category='error')
        else:
            new_product = Product(title=product_title, description=product_description, city=product_city, category=product_category, user_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added!', category='success')

    return render_template("home.html", user=current_user, products=get_all_products)

@views.route('/delete-product', methods=['POST'])
def delete_product():
    data = json.loads(request.data)
    productId = data['productId']
    product = Product.query.get(productId)

    if product:
        if product.user_id == current_user.id:
            db.session.delete(product)
            db.session.commit()
    
    return jsonify({}) # return empty JSON only because returning something is a requirement