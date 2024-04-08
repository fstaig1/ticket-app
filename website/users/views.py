from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm
from website.models import User, Ticket
from .. import db
from datetime import datetime
from werkzeug.security import check_password_hash

users_blueprint = Blueprint("users", __name__, template_folder="/templates")


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Register page to create new User obj from form.

    Renders:
        register.html: on load, on unsuccessful registration

    Redirects:
        users.login: after successful registration
    """
    if current_user.is_authenticated:
        return abort(403, "Forbidden")

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash("A user with this email already exists, try logging in.")
            return render_template("register.html", form=form)

        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=form.password.data,
            role="user",
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Login page to login users.

    Renders:
        login.html: on load, on unsuccessful login

    Redirects:
        next: when forced to login
        admin.admin: when role = admin
        users.profile: when role = user
        venue.venue: when role = venue
    """
    if current_user.is_authenticated:
        return abort(403, "Forbidden")

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            flash("Incorrect login details, please try again.")
            return render_template("login.html", form=form)

        login_user(user)

        user.current_logged_in = datetime.now()

        db.session.add(user)
        db.session.commit()

        next = request.args.get("next")
        if next:
            return redirect(next)

        match current_user.role:
            case "admin":
                return redirect(url_for("admin.admin"))

            case "user":
                return redirect(url_for("users.profile"))

            case "venue":
                return redirect(url_for("venue.venue"))

    return render_template("login.html", form=form)


@users_blueprint.route("/profile")
@login_required
def profile():
    """Profile page to show user details and all their purchased tickets.

    Renders:
        profile.html: on load
    """
    user = User.query.filter_by(id=current_user.id).first()

    tickets = (
        Ticket.query.filter_by(ownerId=current_user.id).filter_by(purchased=True).all()
    )
    tickets.sort(key=lambda ticket: ticket.get_concert().date, reverse=False)

    return render_template("profile.html", current_user=user, tickets=tickets)


@users_blueprint.route("/logout")
def logout():
    """Logs out current user.

    Redirects:
        index: on load
    """
    user = User.query.filter_by(id=current_user.id).first()
    if user:

        user.last_logged_in = user.current_logged_in
        user.current_logged_in = None

        db.session.add(user)
        db.session.commit()

        logout_user()

    return redirect(url_for("index"))
