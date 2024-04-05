from flask import render_template, Blueprint, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..models import Concert, Ticket
from .forms import PurchaseInfoForm
from sqlalchemy import asc
import qrcode

shop_blueprint = Blueprint("shop", __name__, template_folder="/templates")


@shop_blueprint.route("/browse", methods=["POST", "GET"])
def browse():
    global browseConcerts

    match request.form.get("sort_button"):
        case "date":
            browseConcerts = (
                Concert.query.filter(Concert.availableTickets >= 1)
                .order_by(asc(Concert.date))
                .all()
            )

        case "artistName":
            browseConcerts = (
                Concert.query.filter(Concert.availableTickets >= 1)
                .order_by(asc(Concert.artistName))
                .all()
            )

        case "location":
            browseConcerts = (
                Concert.query.filter(Concert.availableTickets >= 1)
                .order_by(asc(Concert.venueLocation))
                .all()
            )

        case "price":
            browseConcerts = (
                Concert.query.filter(Concert.availableTickets >= 1)
                .order_by(asc(Concert.ticketPrice))
                .all()
            )

        case "search":
            print("pass")
            search = request.form.get("search_bar")
            if search:
                found = []
                for concert in browseConcerts:
                    if search.lower() in concert.artistName.lower():
                        found.append(concert)
                return render_template("browse.html", concerts=found)

        case _:
            browseConcerts = (
                Concert.query.filter(Concert.availableTickets >= 1)
                .order_by(asc(Concert.date))
                .all()
            )

    return render_template("browse.html", concerts=browseConcerts)


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

    if concert:
        concert.create_ticket(ownerId=current_user.id)

    return redirect(url_for("shop.cart"))


@shop_blueprint.route("/remove_from_cart", methods=["POST"])
@login_required
def remove_from_cart():

    ticket = Ticket.query.filter_by(
        id=request.form.get("remove_from_cart_button")
    ).first()

    if ticket:
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

    if ticket:
        concert = ticket.get_concert()
        concert.create_ticket(ownerId=current_user.id)

    return redirect(url_for("shop.cart"))


@shop_blueprint.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():
    cart = (
        Ticket.query.filter_by(ownerId=current_user.id).filter_by(purchased=False).all()
    )

    if cart:
        purchaseInfoForm = PurchaseInfoForm()
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
        
    else:
        return abort(403, "Forbidden")


@shop_blueprint.route("/view_ticket", methods=["GET", "POST"])
@login_required
def view_ticket():
    ticket = Ticket.query.filter_by(id=request.form.get("view_ticket_button")).first()

    if ticket:
        confirmationCode = ticket.confirmationCode

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )

        qr.add_data(confirmationCode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("website/static/qr.png")

        return render_template(
            "ticket.html",
            ticket=ticket,
            confirmationCode=confirmationCode,
        )
        
    else:
        return abort(403, "Forbidden")
