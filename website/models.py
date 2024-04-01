from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime
from . import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(100), nullable=False, default="user")

    venueManager = db.Column(db.Boolean(), nullable=False, default=False)
    venueId = db.Column(db.Integer, db.ForeignKey("venues.id"), default=None)

    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    def get_venue(self):
        return Venue.query.filter_by(id=self.venueId).first()

    def delete(self):
        tickets = Ticket.query.filter_by(ownerId=self.id).all()
        for ticket in tickets:
            ticket.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(
        self, firstname, lastname, email, password, role, venueManager, venueId
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None
        self.venueManager = venueManager
        self.venueId = venueId


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def delete(self):
        concerts = Concert.query.filter_by(artistId=self.id).all()
        for concert in concerts:
            concert.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(self, name):
        self.name = name


class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def create_Concert(self, artistId, artistName, ticketPrice, date, availableTickets):
        concert = Concert(
            artistId=artistId,
            artistName=artistName,
            venueId=self.id,
            venueName=self.name,
            venueLocation=self.location,
            ticketPrice=ticketPrice,
            date=date,
            availableTickets=availableTickets,
        )
        db.session.add(concert)
        db.session.commit()
        return concert

    def delete(self):
        concerts = Concert.query.filter_by(venueId=self.id).all()
        for concert in concerts:
            concert.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(self, name, location, capacity):
        self.name = name
        self.location = location
        self.capacity = capacity


class Concert(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True)

    artistId = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artistName = db.Column(db.String(100), nullable=False)

    venueId = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venueName = db.Column(db.String(100), nullable=False)
    venueLocation = db.Column(db.String(100), nullable=False)

    date = db.Column(db.DateTime, nullable=True)
    ticketPrice = db.Column(db.Float, nullable=False)

    availableTickets = db.Column(db.Integer, nullable=False)

    def create_ticket(self, ownerId, purchased):
        ticket = Ticket(ownerId=ownerId, purchased=purchased, concertId=self.id)
        self.availableTickets -= 1
        db.session.add(self)
        db.session.add(ticket)
        db.session.commit()
        return ticket

    def delete(self):
        tickets = Ticket.query.filter_by(concertId=self.artistId).all()
        for ticket in tickets:
            ticket.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(
        self,
        artistId,
        artistName,
        venueId,
        venueName,
        venueLocation,
        ticketPrice,
        date,
        availableTickets,
    ):
        self.artistId = artistId
        self.artistName = artistName
        self.venueId = venueId
        self.venueName = venueName
        self.venueLocation = venueLocation
        self.ticketPrice = ticketPrice
        self.date = date
        self.availableTickets = availableTickets


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)

    ownerId = db.Column(db.Integer, db.ForeignKey(User.id))
    concertId = db.Column(db.Integer, db.ForeignKey(Concert.id))
    purchased = db.Column(db.Boolean, nullable=False)

    def get_concert(self):
        return Concert.query.filter_by(id=self.concertId).first()

    def get_owner(self):
        return User.query.filter_by(id=self.ownerId).first()

    def delete(self):  # FIXME not deleting??
        concert = self.get_concert()
        concert.availableTickets += 1
        db.session.add(concert)
        db.session.delete(self)
        db.session.commit()

    def __init__(self, ownerId, concertId, purchased):
        self.ownerId = ownerId
        self.concertId = concertId
        self.purchased = purchased
