from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') # name of blueprint + .route()
def home():
    return render_template("home.html")
