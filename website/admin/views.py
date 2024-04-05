from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from ..models import User, Venue, Artist, Concert, Ticket
from main import requires_roles
from .forms import CreateUserForm, CreateVenueForm
from .. import db

admin_blueprint = Blueprint("admin", __name__, template_folder="templates")


@admin_blueprint.route("/admin", methods=["GET", "POST"])
@login_required
@requires_roles("admin")
def admin():
    match request.form.get("view_button"):
        case "users":
            return render_template(
                "admin.html",
                current_users=User.query.all(),
                createUserForm=CreateUserForm(),
                createVenueForm=CreateVenueForm(),
            )
        case "venues":
            return render_template(
                "admin.html",
                venues=Venue.query.all(),
                createUserForm=CreateUserForm(),
                createVenueForm=CreateVenueForm(),
            )
        case "artists":
            return render_template(
                "admin.html",
                artists=Artist.query.all(),
                createUserForm=CreateUserForm(),
                createVenueForm=CreateVenueForm(),
            )
        case "concerts":
            return render_template(
                "admin.html",
                concerts=Concert.query.all(),
                createUserForm=CreateUserForm(),
                createVenueForm=CreateVenueForm(),
            )
        case "tickets":
            return render_template(
                "admin.html",
                tickets=Ticket.query.all(),
                createUserForm=CreateUserForm(),
                createVenueForm=CreateVenueForm(),
            )

    return render_template(
        "admin.html", createUserForm=CreateUserForm(), createVenueForm=CreateVenueForm()
    )


@admin_blueprint.route("/admin/delete_user", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_user():
    user = User.query.filter_by(id=request.form.get("delete_user_button")).first()
    user.delete()
    return render_template(
        "admin.html",
        current_users=User.query.all(),
        createUserForm=CreateUserForm(),
        createVenueForm=CreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_venue", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_venue():
    venue = Venue.query.filter_by(id=request.form.get("delete_venue_button")).first()
    venue.delete()
    return render_template(
        "admin.html",
        venues=Venue.query.all(),
        createUserForm=CreateUserForm(),
        createVenueForm=CreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_artist", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_artist():
    artist = Artist.query.filter_by(id=request.form.get("delete_artist_button")).first()
    artist.delete()
    return render_template(
        "admin.html",
        artists=Artist.query.all(),
        createUserForm=CreateUserForm(),
        createVenueForm=CreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_concert", methods=["POST"])
@login_required
@requires_roles("admin")
def delete_concert():
    concert = Concert.query.filter_by(
        id=request.form.get("delete_concert_button")
    ).first()
    concert.delete()
    return render_template(
        "admin.html",
        concerts=Concert.query.all(),
        createUserForm=CreateUserForm(),
        createVenueForm=CreateVenueForm(),
    )


@admin_blueprint.route("/admin/delete_ticket", methods=["GET", "POST"])
@login_required
@requires_roles("admin")
def delete_ticket():
    ticket = Ticket.query.filter_by(id=request.form.get("delete_ticket_button")).first()
    ticket.delete()
    return render_template(
        "admin.html",
        tickets=Ticket.query.all(),
        createUserForm=CreateUserForm(),
        createVenueForm=CreateVenueForm(),
    )


@admin_blueprint.route("/admin/create_user", methods=["POST"])
@login_required
@requires_roles("admin")
def create_user():
    createUserForm = CreateUserForm()
    if createUserForm.validate_on_submit():
        if createUserForm.venueId.data and createUserForm.role.data == "venue":
            venueManager = True
            venueId = createUserForm.venueId.data
        elif not createUserForm.venueId.data and createUserForm.role.data == "venue":
            flash("Venue ID required for venue manager role.")
            return redirect(url_for("admin.admin"))
        else:
            venueManager = False
            venueId = None

        newUser = User(
            firstname=createUserForm.firstname.data,
            lastname=createUserForm.lastname.data,
            email=createUserForm.email.data,
            password=createUserForm.password.data,
            role=createUserForm.role.data,
            venueManager=venueManager,
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
    createVenueForm = CreateVenueForm()
    if createVenueForm.validate_on_submit():
        newVenue = Venue(
            name=createVenueForm.name.data,
            location=createVenueForm.location.data,
            capacity=createVenueForm.capacity.data,
        )
        db.session.add(newVenue)
        db.session.commit()
    else:
        for i in createVenueForm.errors:
            flash(f"{createVenueForm.errors[i][0]}")
    return redirect(url_for("admin.admin"))
