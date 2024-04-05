from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from ..models import User, Venue, Artist, Concert, Ticket
from main import requires_roles
from .forms import AdminCreateUserForm, AdminCreateVenueForm
from .. import db

admin_blueprint = Blueprint("admin", __name__, template_folder="templates")


@admin_blueprint.route("/admin", methods=["GET", "POST"])
@login_required
@requires_roles("admin")
def admin():
    """Loads admin page,  manages view_button

    Renders:
        admin.html: on load, on press of view_button
    """
    match request.form.get("view_button"):
        case "users":
            return render_template(
                "admin.html",
                current_users=User.query.all(),
                createUserForm=AdminCreateUserForm(),
                createVenueForm=AdminCreateVenueForm(),
            )

        case "venues":
            return render_template(
                "admin.html",
                venues=Venue.query.all(),
                createUserForm=AdminCreateUserForm(),
                createVenueForm=AdminCreateVenueForm(),
            )

        case "artists":
            return render_template(
                "admin.html",
                artists=Artist.query.all(),
                createUserForm=AdminCreateUserForm(),
                createVenueForm=AdminCreateVenueForm(),
            )

        case "concerts":
            return render_template(
                "admin.html",
                concerts=Concert.query.all(),
                createUserForm=AdminCreateUserForm(),
                createVenueForm=AdminCreateVenueForm(),
            )

        case "tickets":
            return render_template(
                "admin.html",
                tickets=Ticket.query.all(),
                createUserForm=AdminCreateUserForm(),
                createVenueForm=AdminCreateVenueForm(),
            )

    return render_template(
        "admin.html",
        createUserForm=AdminCreateUserForm(),
        createVenueForm=AdminCreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_user", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_user():
    """Deletes User from db.

    Renders:
        admin.html: on load
    """
    user = User.query.filter_by(id=request.form.get("delete_user_button")).first()

    if user:
        user.delete()

    return render_template(
        "admin.html",
        current_users=User.query.all(),
        createUserForm=AdminCreateUserForm(),
        createVenueForm=AdminCreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_venue", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_venue():
    """Deletes Venue from db.

    Renders:
        admin.html: on load
    """
    venue = Venue.query.filter_by(id=request.form.get("delete_venue_button")).first()

    if venue:
        venue.delete()

    return render_template(
        "admin.html",
        venues=Venue.query.all(),
        createUserForm=AdminCreateUserForm(),
        createVenueForm=AdminCreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_artist", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_artist():
    """Deletes Artist from db.

    Renders:
        admin.html: on load
    """
    artist = Artist.query.filter_by(id=request.form.get("delete_artist_button")).first()

    if artist:
        artist.delete()

    return render_template(
        "admin.html",
        artists=Artist.query.all(),
        createUserForm=AdminCreateUserForm(),
        createVenueForm=AdminCreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_concert", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_concert():
    """Deletes Concert from db.

    Renders:
        admin.html: on load
    """
    concert = Concert.query.filter_by(
        id=request.form.get("delete_concert_button")
    ).first()

    if concert:
        concert.delete()

    return render_template(
        "admin.html",
        concerts=Concert.query.all(),
        createUserForm=AdminCreateUserForm(),
        createVenueForm=AdminCreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_ticket", methods=["GET", "POST"])
@login_required
@requires_roles("admin")
def delete_ticket():
    """Deletes Ticket from db.

    Renders:
        admin.html: on load
    """
    ticket = Ticket.query.filter_by(id=request.form.get("delete_ticket_button")).first()

    if ticket:
        ticket.delete()

    return render_template(
        "admin.html",
        tickets=Ticket.query.all(),
        createUserForm=AdminCreateUserForm(),
        createVenueForm=AdminCreateVenueForm(),
    )


@admin_blueprint.route("/admin/create_user", methods=["POST"])
@login_required
@requires_roles("admin")
def create_user():
    """Creates new user from form.

    Redirects:
        admin.admin: on load, on unsuccessful creation
    """
    createUserForm = AdminCreateUserForm()

    if createUserForm.validate_on_submit():
        if createUserForm.venueId.data and createUserForm.role.data == "venue":
            venueId = createUserForm.venueId.data

        elif not createUserForm.venueId.data and createUserForm.role.data == "venue":
            flash("Venue ID required for venue manager role.")

            return redirect(url_for("admin.admin"))

        else:
            venueId = None

        newUser = User(
            firstname=createUserForm.firstname.data,
            lastname=createUserForm.lastname.data,
            email=createUserForm.email.data,
            password=createUserForm.password.data,
            role=createUserForm.role.data,
            venueId=venueId,
        )

        db.session.add(newUser)
        db.session.commit()

    else:
        for i in createUserForm.errors:
            flash(f"{createUserForm.errors[i][0]}")

    return redirect(url_for("admin.admin"))


@admin_blueprint.route("/admin/create_venue", methods=["POST"])
@login_required
@requires_roles("admin")
def create_venue():
    """Creates new venue from form.

    Redirects:
        admin.admin: on load, on unsuccessful creation
    """
    adminCreateVenueForm = AdminCreateVenueForm()

    if adminCreateVenueForm.validate_on_submit():
        manager = User.query.filter_by(id=adminCreateVenueForm.managerId.data).first()

        if not manager:
            flash(f"No user with id = {adminCreateVenueForm.managerId.data}")
            return redirect(url_for("admin.admin"))

        if manager.role == "admin":
            flash("You cannot make an admin a venue manager.")
            return redirect(url_for("admin.admin"))

        if manager.role == "venue" and manager.venueId:
            flash(f"User ID {manager.id} already manages a venue.")
            return redirect(url_for("admin.admin"))

        newVenue = Venue(
            name=adminCreateVenueForm.name.data,
            location=adminCreateVenueForm.location.data,
            capacity=adminCreateVenueForm.capacity.data,
        )

        db.session.add(newVenue)
        db.session.commit()

        manager.role = "venue"
        manager.venueId = newVenue.id

        db.session.add(manager)
        db.session.commit()

    else:
        for i in adminCreateVenueForm.errors:
            flash(f"{adminCreateVenueForm.errors[i][0]}")

    return redirect(url_for("admin.admin"))
