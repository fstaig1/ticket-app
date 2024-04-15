from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User, Venue, Concert, Artist
from main import requires_roles
from .forms import CreateConcertForm, CreateVenueForm
from .. import db
from datetime import datetime

venue_blueprint = Blueprint("venue", __name__, template_folder="templates")


@venue_blueprint.route("/venue")
@login_required
@requires_roles("venue")
def venue():
    """Venue page to show user and venue details.

    Renders:
        venue.html: on load
    """

    return render_template(
        "venue.html",
        managers=User.query.filter_by(venueId=current_user.venueId).all(),
        venue=Venue.query.filter_by(id=current_user.venueId).first(),
        concerts=Concert.query.filter_by(venueId=current_user.venueId).all(),
        createConcertForm=CreateConcertForm(),
        createVenueForm=CreateVenueForm(),
    )


@venue_blueprint.route("/venue/create_concert", methods=["POST"])
@requires_roles("venue")
@login_required
def create_concert():
    """Creates new Concert obj at this venue from form. Creates new Artist if required.

    Renders:
        venue.html: on unsuccessful creation

    Redirects:
        venue.venue: on successful creation
    """
    createConcertForm = CreateConcertForm()

    if createConcertForm.validate_on_submit():
        artist = Artist.query.filter_by(
            name=str(createConcertForm.artistName.data).strip()
        ).first()

        if not artist:
            artist = Artist(name=str(createConcertForm.artistName.data).strip())
            db.session.add(artist)
            db.session.commit

        venue = Venue.query.filter_by(id=current_user.venueId).first()

        venue.create_Concert(
            artistId=artist.id,
            artistName=str(artist.name).strip(),
            ticketPrice=int(createConcertForm.ticketPrice.data),
            date=datetime.strptime(
                createConcertForm.date.raw_data[0], "%Y-%m-%dT%H:%M"
            ),
            availableTickets=createConcertForm.capacity.data,
        )

        flash("Concert successfully created.", "alert alert-success")

        return redirect(url_for("venue.venue"))

    return render_template(
        "venue.html",
        managers=User.query.filter_by(venueId=current_user.venueId).all(),
        venue=Venue.query.filter_by(id=current_user.venueId).first(),
        concerts=Concert.query.filter_by(venueId=current_user.venueId),
        createConcertForm=CreateConcertForm(),
        createVenueForm=CreateVenueForm(),
    )


@venue_blueprint.route("/venue/delete_concert", methods=["POST"])
@login_required
@requires_roles("venue")
def delete_concert():
    """Deletes concert by press of delete_concert_button.

    Redirects:
        venue.venue: on load
    """
    concert = Concert.query.filter_by(
        id=request.form.get("delete_concert_button")
    ).first()

    if concert:
        concert.delete()

        flash("Concert successfully deleted.", "alert alert-success")

    return redirect(url_for("venue.venue"))


@venue_blueprint.route("/venue/create_venue", methods=["POST"])
@login_required
@requires_roles("venue")
def create_venue():
    """Creates new Venue obj from form. Updates User to be a venue manager.

    Renders:
        venue.html: on unsuccessful creation

    Redirects:
        venue.venue: on successful creation
    """
    createVenueForm = CreateVenueForm()

    if createVenueForm.validate_on_submit():
        venue = (
            Venue.query.filter_by(name=str(createVenueForm.name.data).strip())
            .filter_by(location=str(createVenueForm.location.data).strip())
            .first()
        )

        if venue:
            flash(
                "A venue with that name and location already exists.",
                "alert alert-danger",
            )
            return redirect(url_for("venue.venue"))

        newVenue = Venue(
            name=str(createVenueForm.name.data).strip(),
            location=str(createVenueForm.location.data).strip(),
            capacity=createVenueForm.capacity.data,
        )

        db.session.add(newVenue)
        db.session.commit()

        manager = User.query.filter_by(id=current_user.id).first()
        manager.role = "venue"
        manager.venueId = newVenue.id

        db.session.add(manager)
        db.session.commit()

        flash("Venue successfully created.", "alert alert-success")

        return redirect(url_for("venue.venue"))

    return render_template(
        "venue.html",
        user=User.query.filter_by(id=current_user.id).first(),
        venue=Venue.query.filter_by(id=current_user.venueId).first(),
        concerts=Concert.query.filter_by(venueId=current_user.venueId),
        createConcertForm=CreateConcertForm(),
        createVenueForm=CreateVenueForm(),
    )
