from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Venue, Concert, Artist
from main import requires_roles
from .forms import ConcertForm
from .. import db
from datetime import datetime

venue_blueprint = Blueprint('venue', __name__, template_folder='templates')


@venue_blueprint.route('/venue')
@login_required
@requires_roles('venue')
def venue():
    concertForm = ConcertForm()
    user = User.query.filter_by(id=current_user.id).first()
    venue = Venue.query.filter_by(id=current_user.venueId).first()
    concerts = Concert.query.filter_by(venueId=current_user.venueId)

    return render_template('venue.html', user=user, venue=venue, concerts=concerts, form=concertForm)


@venue_blueprint.route('/venue/create_concert', methods=['POST'])
@requires_roles('venue')
def create_concert():
    concertForm = ConcertForm()

    if concertForm.validate_on_submit():
        artist = Artist.query.filter_by(name=concertForm.artistName.data).first()
        if not artist:
            artist = Artist(name=concertForm.artistName.data)
            db.session.add(artist)
            db.session.commit

        venue = Venue.query.filter_by(id=current_user.venueId).first()

        venue.create_Concert(artistId=artist.id,
                             artistName=artist.name,
                             ticketPrice=int(concertForm.ticketPrice.data),
                             date=datetime.strptime(concertForm.date.raw_data[0], '%Y-%m-%dT%H:%M'))
    else:
        for i in concertForm.errors.values():
            flash(f'{i[0]}')
    return redirect(url_for('venue.venue'))
