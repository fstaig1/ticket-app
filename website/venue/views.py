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
    user = User.query.filter_by(id=current_user.id).first()
    venue = Venue.query.filter_by(id=current_user.venueId).first()
    concerts = Concert.query.filter_by(venueId=current_user.venueId)

    return render_template(
        "venue.html",
        user=user,
        venue=venue,
        concerts=concerts,
        createConcertForm=CreateConcertForm(),
        createVenueForm=CreateVenueForm(),
    )


@venue_blueprint.route("/venue/create_concert", methods=["POST"])
@requires_roles("venue")
def create_concert():
    """Creates new Concert obj at this venue from form. Creates new Artist if required.

    Redirects:
        venue.venue: on load
    """
    createConcertForm = CreateConcertForm()

    if createConcertForm.validate_on_submit():
        artist = Artist.query.filter_by(name=createConcertForm.artistName.data).first()

        if not artist:
            artist = Artist(name=createConcertForm.artistName.data)
            db.session.add(artist)
            db.session.commit

        venue = Venue.query.filter_by(id=current_user.venueId).first()

        venue.create_Concert(
            artistId=artist.id,
            artistName=artist.name,
            ticketPrice=int(createConcertForm.ticketPrice.data),
            date=datetime.strptime(
                createConcertForm.date.raw_data[0], "%Y-%m-%dT%H:%M"
            ),
            availableTickets=createConcertForm.capacity.data,
        )

    else:
        for i in createConcertForm.errors.values():
            flash(f"{i[0]}")

    return redirect(url_for("venue.venue"))


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

    return redirect(url_for("venue.venue"))


@venue_blueprint.route("/venue/create_venue", methods=["POST"])
@login_required
@requires_roles("venue")
def create_venue():
    """Creates new Venue obj from form. Updates User to be a venue manager.

    Redirects:
        venue.venue: on load
    """
    createVenueForm = CreateVenueForm()

    if createVenueForm.validate_on_submit():
        newVenue = Venue(
            name=createVenueForm.name.data,
            location=createVenueForm.location.data,
            capacity=createVenueForm.capacity.data,
        )

        db.session.add(newVenue)
        db.session.commit()

        manager = User.query.filter_by(id=current_user.id).first()
        manager.role = "venue"
        manager.venueId = newVenue.id

        db.session.add(manager)
        db.session.commit()

    else:
        for i in createVenueForm.errors:
            flash(f"{createVenueForm.errors[i][0]}")

    return redirect(url_for("venue.venue"))
