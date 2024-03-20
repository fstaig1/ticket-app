from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm 
from website.models import User
from .. import db
from datetime import datetime
from werkzeug.security import check_password_hash

users_blueprint = Blueprint('users', __name__, template_folder='/templates')


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


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Incorrect login details, please try again.")
            return render_template('login.html', form=form)

        login_user(user)
        user.last_logged_in = user.current_logged_in
        user.current_logged_in = datetime.now()
        db.session.add(user)
        db.session.commit()
        
        match current_user.role:
            case 'admin': return redirect(url_for('admin.admin'))
            case 'venue': return redirect(url_for('venue.venue'))
            case 'user' : return redirect(url_for('users.profile'))
        
    return render_template('login.html', form=form)


@users_blueprint.route('/profile')
def profile():
    return render_template('profile.html')

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
