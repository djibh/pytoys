from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Product
from . import db, app

import os, json

views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
filename = ""

@views.route('/', methods=['GET'])
@login_required
def home():
    get_all_products = db.session.query(Product).all()
    return render_template("home.html", user=current_user, products=get_all_products)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_picture():
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
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('views.home', name=filename))


@views.route('/account', methods=['POST', 'GET'])
def upload_product():
    if request.method == 'POST':
        product_title = request.form.get('product-title')
        product_description = request.form.get('product-description')
        product_category = request.form.get('product-category')
        product_city = request.form.get('product-city')

        if len(product_title) < 1:
            flash('Product\'s description is too short!', category='error')
        else:
            upload_picture()
            new_product = Product(title=product_title, description=product_description, pictures=filename, city=product_city, category=product_category, user_id=current_user.id)
            print(new_product)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added!', category='success')

    return render_template("account.html", user=current_user)


@views.route('/product/<id>', methods=['POST', 'GET'])
def show_product(id):
    product_id = id
    product = Product.query.filter_by(id=product_id).first()

    return render_template("product.html", user=current_user, product=product)


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

@views.route('/test-fetch', methods=['GET'])
def show_data():
    return {
            'Name':"geek",
            "Age":22,
            "programming":"python"
            }