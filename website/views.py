from flask import Blueprint, current_app as app, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Product
from . import db

import os, json

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    get_all_products = db.session.query(Product).all()
    return render_template("home.html", user=current_user, products=get_all_products)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/account', methods=['POST', 'GET'])
def upload_file():
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

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('views.home', name=filename))

    return render_template("account.html", user=current_user)


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