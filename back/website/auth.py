from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Product
from . import db

auth = Blueprint('auth', __name__)
    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        password_confirmation = request.form.get('password-conf')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != password_confirmation:
            flash('Passwords must be identical.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/account', methods=['GET', 'POST'])
def account():
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

    return render_template("account.html", user=current_user)