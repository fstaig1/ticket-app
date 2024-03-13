from flask import Blueprint, render_template, flash, redirect, url_for
from users.forms import RegisterForm
from models import User
from app import db

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('A user with this email already exists, try logging in.')
            return render_template('register.html', form=form)
        
        new_user = User(firstname=form.firstname.data, 
                        lastname=form.lastname.data,
                        email=form.email.data,
                        password=form.password.data,
                        role="user")
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('users.login'))
        
    return render_template('register.html', form=form)

@users_blueprint.route('/login')
def login():
    return render_template('login.html')



@users_blueprint.route('/profile')
def profile():
    return render_template('profile.html')

@users_blueprint.route('/logout')
def logout():
    return render_template('index.html')
