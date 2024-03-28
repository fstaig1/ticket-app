from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User, Venue, Concert, Artist
# from main import requires_roles
# from .. import db
# from datetime import datetime
from sqlalchemy import asc

shop_blueprint = Blueprint('shop', __name__, template_folder='/templates')


@shop_blueprint.route('/browse')
def browse():
    global concerts
    concerts = Concert.query.order_by(asc(Concert.date)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_date', methods=['POST'])
def sort_by_date():
    concerts = Concert.query.order_by(asc(Concert.date)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_name', methods=['POST'])
def sort_by_name():
    concerts = Concert.query.order_by(asc(Concert.artistName)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_location', methods=['POST'])
def sort_by_location():
    concerts = Concert.query.order_by(asc(Concert.venueLocation)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_price', methods=['POST'])
def sort_by_price():
    concerts = Concert.query.order_by(asc(Concert.ticketPrice)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/purchase', methods=['POST'])
@login_required
def ticket_page():
    concert = Concert.query.filter_by(id=request.form.get("purchase_button")).first()
    user = User.query.filter_by(id=current_user.id).first()
    print(concert)
    return render_template('purchase.html', concert=concert)
