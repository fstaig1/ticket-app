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
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    match request.form.get("view_button"):
        case "users":
            return render_template(
                "admin.html",
                current_users=User.query.all(),
                createUserForm=adminCreateUserForm,
                createVenueForm=adminCreateVenueForm,
            )

        case "venues":
            return render_template(
                "admin.html",
                venues=Venue.query.all(),
                createUserForm=adminCreateUserForm,
                createVenueForm=adminCreateVenueForm,
            )

        case "artists":
            return render_template(
                "admin.html",
                artists=Artist.query.all(),
                createUserForm=adminCreateUserForm,
                createVenueForm=adminCreateVenueForm,
            )

        case "concerts":
            return render_template(
                "admin.html",
                concerts=Concert.query.all(),
                createUserForm=adminCreateUserForm,
                createVenueForm=adminCreateVenueForm,
            )

        case "tickets":
            return render_template(
                "admin.html",
                tickets=Ticket.query.all(),
                createUserForm=adminCreateUserForm,
                createVenueForm=adminCreateVenueForm,
            )

    return render_template(
        "admin.html",
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/delete_user", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_user():
    """Deletes User from db.

    Renders:
        admin.html: on load
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    user = User.query.filter_by(id=request.form.get("delete_user_button")).first()

    if user:
        user.delete()

        flash("User successfully deleted.", "alert alert-success")

    return render_template(
        "admin.html",
        current_users=User.query.all(),
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/delete_venue", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_venue():
    """Deletes Venue from db.

    Renders:
        admin.html: on load
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    venue = Venue.query.filter_by(id=request.form.get("delete_venue_button")).first()

    if venue:
        venue.delete()

        flash("Venue successfully deleted.", "alert alert-success")

    return render_template(
        "admin.html",
        venues=Venue.query.all(),
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/delete_artist", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_artist():
    """Deletes Artist from db.

    Renders:
        admin.html: on load
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    artist = Artist.query.filter_by(id=request.form.get("delete_artist_button")).first()

    if artist:
        artist.delete()

        flash("Artist successfully deleted.", "alert alert-success")

    return render_template(
        "admin.html",
        artists=Artist.query.all(),
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/delete_concert", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_concert():
    """Deletes Concert from db.

    Renders:
        admin.html: on load
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    concert = Concert.query.filter_by(
        id=request.form.get("delete_concert_button")
    ).first()

    if concert:
        concert.delete()

        flash("Concert successfully deleted.", "alert alert-success")

    return render_template(
        "admin.html",
        concerts=Concert.query.all(),
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/delete_ticket", methods=["GET", "POST"])
@login_required
@requires_roles("admin")
def delete_ticket():
    """Deletes Ticket from db.

    Renders:
        admin.html: on load
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    ticket = Ticket.query.filter_by(id=request.form.get("delete_ticket_button")).first()

    if ticket:
        ticket.delete()

        flash("Ticket successfully deleted.", "alert alert-success")

    return render_template(
        "admin.html",
        tickets=Ticket.query.all(),
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/create_user", methods=["POST"])
@login_required
@requires_roles("admin")
def create_user():
    """Creates new user from form.

    Renders:
        admin.html: on unsuccessful creation

    Redirects:
        admin.admin: on successful creation
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    if adminCreateUserForm.validate_on_submit():
        valid = True
        user = User.query.filter_by(
            email=str(adminCreateUserForm.email.data).strip()
        ).first()

        if user:
            flash("A user with this email already exists", "alert alert-danger")
            valid = False

        if (
            adminCreateUserForm.venueId.data
            and str(adminCreateUserForm.role.data).strip() == "venue"
        ):
            venueId = adminCreateUserForm.venueId.data

        elif (
            not adminCreateUserForm.venueId.data
            and str(adminCreateUserForm.role.data).strip() == "venue"
        ):
            flash("Venue ID required for venue manager role.", "alert alert-danger")

            valid = False

        else:
            venueId = None

        if valid:
            newUser = User(
                firstname=str(adminCreateUserForm.firstname.data).strip(),
                lastname=str(adminCreateUserForm.lastname.data).strip(),
                email=str(adminCreateUserForm.email.data).strip(),
                password=str(adminCreateUserForm.password.data).strip(),
                role=adminCreateUserForm.role.data,
                venueId=venueId,
            )

            db.session.add(newUser)
            db.session.commit()

            flash("User successfully created.", "alert alert-success")

            return redirect(url_for("admin.admin"))

    return render_template(
        "admin.html",
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )


@admin_blueprint.route("/admin/create_venue", methods=["POST"])
@login_required
@requires_roles("admin")
def create_venue():
    """Creates new venue from form.

    Renders:
        admin.html: on unsuccessful creation

    Redirects:
        admin.admin: on successful creation
    """
    adminCreateUserForm = AdminCreateUserForm()
    adminCreateVenueForm = AdminCreateVenueForm()

    if adminCreateVenueForm.validate_on_submit():
        venue = Venue.query.filter_by(
            name=str(adminCreateVenueForm.name.data).strip(),
            location=str(adminCreateVenueForm.location.data).strip(),
        ).first()

        if venue:
            flash(
                "A venue with that name and location already exists.",
                "alert alert-danger",
            )
            return redirect(url_for("admin.admin"))

        manager = User.query.filter_by(id=adminCreateVenueForm.managerId.data).first()

        if not manager:
            flash(
                f"No user with id = {adminCreateVenueForm.managerId.data}",
                "alert alert-danger",
            )
            return redirect(url_for("admin.admin"))

        if manager.role == "admin":
            flash("You cannot make an admin a venue manager.", "alert alert-danger")
            return redirect(url_for("admin.admin"))

        if manager.role == "venue" and manager.venueId:
            flash(
                f"User ID {manager.id} already manages a venue.", "alert alert-danger"
            )
            return redirect(url_for("admin.admin"))

        newVenue = Venue(
            name=str(adminCreateVenueForm.name.data).strip(),
            location=str(adminCreateVenueForm.location.data).strip(),
            capacity=adminCreateVenueForm.capacity.data,
        )

        db.session.add(newVenue)
        db.session.commit()

        manager.role = "venue"
        manager.venueId = newVenue.id

        db.session.add(manager)
        db.session.commit()

        flash("Venue successfully created.", "alert alert-success")

        return redirect(url_for("admin.admin"))

    return render_template(
        "admin.html",
        createUserForm=adminCreateUserForm,
        createVenueForm=adminCreateVenueForm,
    )
