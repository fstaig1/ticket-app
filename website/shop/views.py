from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Concert, Ticket
from .forms import PurchaseInfoForm
from sqlalchemy import asc
import qrcode

shop_blueprint = Blueprint("shop", __name__, template_folder="/templates")


@shop_blueprint.route("/browse")
def browse():
    concerts = (
        Concert.query.filter(Concert.availableTickets >= 1)
        .order_by(asc(Concert.date))
        .all()
    )
    return render_template("browse.html", concerts=concerts)


@shop_blueprint.route("/browse/sort_by_date", methods=["POST"])
def sort_by_date():
    concerts = (
        Concert.query.filter(Concert.availableTickets >= 1)
        .order_by(asc(Concert.date))
        .all()
    )
    return render_template("browse.html", concerts=concerts)


@shop_blueprint.route("/browse/sort_by_name", methods=["POST"])
def sort_by_name():
    concerts = (
        Concert.query.filter(Concert.availableTickets >= 1)
        .order_by(asc(Concert.artistName))
        .all()
    )
    return render_template("browse.html", concerts=concerts)


@shop_blueprint.route("/browse/sort_by_location", methods=["POST"])
def sort_by_location():
    concerts = (
        Concert.query.filter(Concert.availableTickets >= 1)
        .order_by(asc(Concert.venueLocation))
        .all()
    )
    return render_template("browse.html", concerts=concerts)


@shop_blueprint.route("/browse/sort_by_price", methods=["POST"])
def sort_by_price():
    concerts = (
        Concert.query.filter(Concert.availableTickets >= 1)
        .order_by(asc(Concert.ticketPrice))
        .all()
    )
    return render_template("browse.html", concerts=concerts)


@shop_blueprint.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    cart = (
        Ticket.query.filter_by(ownerId=current_user.id).filter_by(purchased=False).all()
    )
    return render_template("cart.html", user=current_user, cart=cart)


@shop_blueprint.route("/add_to_cart", methods=["POST"])
@login_required
def add_to_cart():
    concert = Concert.query.filter_by(id=request.form.get("purchase_button")).first()
    concert.create_ticket(ownerId=current_user.id, purchased=False)
    return redirect(url_for("shop.cart"))


@shop_blueprint.route("/remove_from_cart", methods=["POST"])
@login_required
def remove_from_cart():
    ticket = Ticket.query.filter_by(
        id=request.form.get("remove_from_cart_button")
    ).first()
    ticket.delete()
    return redirect(url_for("shop.cart"))


@shop_blueprint.route("/empty_cart", methods=["GET", "POST"])
@login_required
def empty_cart():
    cart = (
        Ticket.query.filter_by(ownerId=current_user.id).filter_by(purchased=False).all()
    )

    for ticket in cart:
        ticket.delete()

    return redirect(url_for("shop.cart"))


@shop_blueprint.route("/buy_additional_ticket", methods=["POST"])
@login_required
def buy_additional_ticket():
    ticket = Ticket.query.filter_by(
        id=request.form.get("buy_additional_ticket_button")
    ).first()
    concert = ticket.get_concert()
    concert.create_ticket(ownerId=current_user.id, purchased=False)
    return redirect(url_for("shop.cart"))


@shop_blueprint.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():
    purchaseInfoForm = PurchaseInfoForm()
    cart = (
        Ticket.query.filter_by(ownerId=current_user.id).filter_by(purchased=False).all()
    )
    totalPrice = 0
    for item in cart:
        totalPrice += item.get_concert().ticketPrice

    if purchaseInfoForm.validate_on_submit():
        # this is where you would run code to process card details and make a transaction
        # im obviously not going to do that here because that would break the ethics agreement
        # but i sure can simulate it
        for item in cart:
            item.purchase_ticket()

        return render_template("reciept.html", cart=cart, totalPrice=totalPrice)
    else:
        for error in purchaseInfoForm.errors:
            flash(f"{purchaseInfoForm.errors[error][0]}")

    return render_template(
        "purchase.html",
        form=purchaseInfoForm,
        user=current_user,
        cart=cart,
        totalPrice=totalPrice,
    )


@shop_blueprint.route("/view_ticket", methods=["GET", "POST"])
@login_required
def view_ticket():
    ticket = Ticket.query.filter_by(id=request.form.get("view_ticket")).first()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"AAA")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/qr.png")

    return render_template("ticket.html", ticket=ticket, user=current_user)
