from flask import Blueprint, render_template

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register')
def register():
    return render_template('register.html')

@users_blueprint.route('/login')
def login():
    return render_template('login.html')

@users_blueprint.route('/profile')
def profile():
    return render_template('profile.html')

@users_blueprint.route('/logout')
def logout():
    return render_template('index.html')
