from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User, Venue, Concert, Artist, Ticket
# from main import requires_roles
from .. import db
# from datetime import datetime
from .forms import PurchaseInfoForm
from sqlalchemy import asc

shop_blueprint = Blueprint('shop', __name__, template_folder='/templates')


@shop_blueprint.route('/browse')
def browse():
    concerts = Concert.query.\
        filter(Concert.availableTickets >= 1).\
        order_by(asc(Concert.date)).\
        all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_date', methods=['POST'])
def sort_by_date():
    concerts = Concert.query.\
        filter(Concert.availableTickets >= 1).\
        order_by(asc(Concert.date)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_name', methods=['POST'])
def sort_by_name():
    concerts = Concert.query.\
        filter(Concert.availableTickets >= 1).\
        order_by(asc(Concert.artistName)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_location', methods=['POST'])
def sort_by_location():
    concerts = Concert.query.\
        filter(Concert.availableTickets >= 1).\
        order_by(asc(Concert.venueLocation)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/browse/sort_by_price', methods=['POST'])
def sort_by_price():
    concerts = Concert.query.\
        filter(Concert.availableTickets >= 1).\
        order_by(asc(Concert.ticketPrice)).all()
    return render_template('browse.html', concerts=concerts)


@shop_blueprint.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart = Ticket.query.\
        filter_by(ownerId=current_user.id).\
        filter_by(purchased=False).all()
    return render_template('cart.html', user=current_user, cart=cart)


@shop_blueprint.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    concert = Concert.query.filter_by(id=request.form.get("purchase_button")).first()
    concert.create_ticket(ownerId=current_user.id,
                          purchased=False)
    return redirect(url_for('shop.cart'))


@shop_blueprint.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    ticket = Ticket.query.filter_by(id=request.form.get("remove_from_cart_button")).first()
    ticket.delete()
    return redirect(url_for('shop.cart'))


@shop_blueprint.route('/buy_additional_ticket', methods=['POST'])
@login_required
def buy_additional_ticket():
    ticket = Ticket.query.filter_by(id=request.form.get("buy_additional_ticket_button")).first()
    concert = ticket.get_concert()
    concert.create_ticket(ownerId=current_user.id,
                          purchased=False)
    return redirect(url_for('shop.cart'))
