from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Product
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        product = request.form.get('product')

        if len(product) < 1:
            flash('Product\'s description is too short!', category='error')
        else:
            new_product = Product(description=product, user_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added!', category='success')

    return render_template("home.html", user=current_user)

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