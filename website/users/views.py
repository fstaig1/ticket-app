from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, ProfileForm
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
        users.profile: after successful registration
    """
    if current_user.is_authenticated:
        return abort(403, "Forbidden")

    registerForm = RegisterForm()

    if registerForm.validate_on_submit():
        user = User.query.filter_by(email=str(registerForm.email.data).strip()).first()

        if user:
            flash(
                "A user with this email already exists, try logging in.",
                "alert alert-danger",
            )
            return render_template("register.html", form=registerForm)

        new_user = User(
            firstname=str(registerForm.firstname.data).strip(),
            lastname=str(registerForm.lastname.data).strip(),
            email=str(registerForm.email.data).strip(),
            password=str(registerForm.password.data).strip(),
            role="user",
        )

        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=str(registerForm.email.data).strip()).first()

        login_user(user)

        user.current_logged_in = datetime.now()

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("users.profile"))

    return render_template("register.html", form=registerForm)


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

    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=str(loginForm.email.data).strip()).first()

        if not user or not check_password_hash(
            user.password, str(loginForm.password.data).strip()
        ):
            flash("Incorrect login details, please try again.", "alert alert-danger")
            return render_template("login.html", form=loginForm)

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

    return render_template("login.html", form=loginForm)


@users_blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Profile page to show user details and all their purchased tickets.

    Renders:
        profile.html: on load
    """
    profileForm = ProfileForm()

    tickets = (
        Ticket.query.filter_by(ownerId=current_user.id).filter_by(purchased=True).all()
    )
    tickets.sort(key=lambda ticket: ticket.get_concert().date, reverse=False)

    if profileForm.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()

        user.change_password(str(profileForm.password.data).strip())

        flash("Password successfully changed.", "alert alert-success")

    return render_template("profile.html", tickets=tickets, form=profileForm)


@users_blueprint.route("/logout")
def logout():
    """Logs out current user.

    Redirects:
        index: on load
    """

    if not current_user.is_authenticated:
        return abort(403, "Forbidden")

    user = User.query.filter_by(id=current_user.id).first()

    user.last_logged_in = user.current_logged_in
    user.current_logged_in = None

    db.session.add(user)
    db.session.commit()

    logout_user()

    return redirect(url_for("index"))
