from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime
from . import db
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from zlib import compress, decompress


class User(db.Model, UserMixin):
    """User class / 'users' database table

    Args:
        id (int): users unique id
        firstname (str): user's first name
        lastname (str): user's last name
        email (str): user's email address
        password (str): user's hashed password
        role (str): user's role, either admin/user/venue
        venueId (int): id of venue
        registered_on (datetime): date and time of when user was created
        last_logged_in (datetime): date and time of last user login
        current_logged_in (datetime): date and time of when the user logged in if currently logged in

    Methods:
        get_venue: Gets Venue where id equals own venueId.
        change_password: hashes and changes self's password to param value
        delete: Deletes all user's tickets from db and then self.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=False, default="user")
    venueId = db.Column(db.Integer, db.ForeignKey("venues.id"), default=None)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    def get_venue(self):
        """Gets Venue where id equals own venueId

        Returns:
            Venue obj: venue object with users venueid
        """
        return Venue.query.filter_by(id=self.venueId).first()

    def change_password(self, newPassword: str):
        """Hashes password arg and sets self.password to it

        Args:
            newPassword (str): string to set new password to

        Returns:
            string: hashed password
        """
        self.password = generate_password_hash(newPassword)

        db.session.add(self)
        db.session.commit()

        return self.password

    def delete(self):
        """Deletes all user's tickets from db and then self."""
        tickets = Ticket.query.filter_by(ownerId=self.id).all()

        for ticket in tickets:
            ticket.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(
        self,
        firstname: str,
        lastname: str,
        email: str,
        password: str,
        role: str,
        venueId: int = None,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None
        self.venueId = venueId


class Artist(db.Model):
    """Artist class / 'artists' database table

    Args:
        id (int): artist's unique id
        name (str): artist's name

    Methods:
        delete: Deletes all artists's concerts from db and then self.
    """

    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def delete(self):
        """Deletes all artists's concerts from db and then self."""
        concerts = Concert.query.filter_by(artistId=self.id).all()

        for concert in concerts:
            concert.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(self, name: str):
        self.name = name


class Venue(db.Model):
    """Venue class / 'venues' database table

    Args:
        id (int): venues's unique id
        name (str): venue's name
        location (str): venue's location
        capacity (int): venue's capacity

    Methods:
        create_Concert: creates new Concert at this venue
        delete: Deletes all of this venue's concerts from db, and then deletes self from db.
    """

    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def create_Concert(
        self,
        artistId: int,
        artistName: str,
        ticketPrice: int,
        date: datetime,
        availableTickets: int,
    ):
        """creates Concert object for this venue

        Args:
            artistId (int): artist's unique id
            artistName (str): artist's name
            ticketPrice (int): ticket price
            date (datetime): date and time of concert
            availableTickets (int): amount of remaining tickets

        Returns:
            Concert obj: Concert object created by this method
        """
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
        """Deletes all of this venue's concerts from db, and then deletes self from db."""
        concerts = Concert.query.filter_by(venueId=self.id).all()

        for concert in concerts:
            concert.delete()

        manager = User.query.filter_by(venueId=self.id).first()
        if manager:
            manager.venueId = None
            db.session.add(manager)

        db.session.delete(self)
        db.session.commit()

    def __init__(self, name: str, location: str, capacity: int):
        self.name = name
        self.location = location
        self.capacity = capacity


class Concert(db.Model):
    """Concert class / 'concerts' database table

    Args:
        id (int): concert's unique id
        artistId (int): artist's unique id
        artistName (str): artists name
        venueId (int): venue's  unique id
        venueName (str): venue's name
        venueLocation (str): venue's location
        date  (datetime): date and time of concert
        ticketPrice (int): price of ticket
        availableTickets (int): amount of remaining tickets

    Methods:
        create_ticket: creates Ticket obj for this concert
        delete: Deletes all tickets for this concert from the db, and then self.
    """

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

    def create_ticket(self, ownerId: int):
        """creates Ticket obj for this concert

        Args:
            ownerId (int): unique user id of ticket owner

        Returns:
            Ticket obj: Ticket obj created by this method
        """
        ticket = Ticket(ownerId=ownerId, concertId=self.id)
        self.availableTickets -= 1

        db.session.add(self)
        db.session.add(ticket)
        db.session.commit()

        return ticket

    def delete(self):
        """Deletes all tickets for this concert from the db, and then self."""
        tickets = Ticket.query.filter_by(concertId=self.id).all()

        for ticket in tickets:
            ticket.delete()

        db.session.delete(self)
        db.session.commit()

    def __init__(
        self,
        artistId: int,
        artistName: str,
        venueId: int,
        venueName: str,
        venueLocation: str,
        ticketPrice: int,
        date: datetime,
        availableTickets: int,
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
    """Ticket Class / 'tickets' database table

    Args:
        id (int): ticket's unique id
        ownerId (int): unique id of the user who owns this ticket
        concertId (int): unique id of the concert this ticket is for
        purchased (bool): True/False if ticket is purchased
        confirmationCode (str): base64 string for qrcode

    Methods:
        get_concert: Gets Concert where id equals own concertId
        get_owner: Gets User where id equals own ownerId
        encode: compresses and converts concertId + ownerId into base64
        decode: decompresses and converts base64 into concertId + ownerId
        purchase_ticket: changes self.purchased to be True, creates confirmation code
        delete: Deletes self and increases available tickets
    """

    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, db.ForeignKey(User.id))
    concertId = db.Column(db.Integer, db.ForeignKey(Concert.id))
    purchased = db.Column(db.Boolean, nullable=False)
    confirmationCode = db.Column(db.String(255), nullable=True)

    def get_concert(self):
        """Gets Concert where id equals own concertId

        Returns:
            _type_: _description_
        """
        return Concert.query.filter_by(id=self.concertId).first()

    def get_owner(self):
        """Gets User where id equals own ownerId

        Returns:
            _type_: _description_
        """
        return User.query.filter_by(id=self.ownerId).first()

    def encode(self):
        """compresses and converts concertId + ownerId into base64

        Returns:
            bytes: string containing ticketId + concertId + ownerId converted into base64
        """
        return b64e(
            compress(
                (
                    b"ticketId: %d, concertId:%d, ownerId:%d"
                    % (self.id, self.get_concert().id, self.get_owner().id)
                ),
                9,
            )
        )

    def decode(self):  # not used but would potentially be useful for future work
        """decompresses and converts base64 into concertId + ownerId

        Returns:
            bytes: string containing ticketId + concertId + ownerId
        """
        return decompress(b64d(bytes(self.confirmationCode, "utf-8")))

    def purchase_ticket(self):
        """changes self.purchased to be True, creates confirmation code"""
        self.purchased = True
        self.confirmationCode = str(self.encode(), "utf-8")

        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes self and increases available tickets"""
        concert = self.get_concert()
        concert.availableTickets += 1

        db.session.add(concert)
        db.session.delete(self)
        db.session.commit()

    def __init__(
        self,
        ownerId: int,
        concertId: int,
        purchased: bool = False,
        confimationCode: str = None,
    ):
        self.ownerId = ownerId
        self.concertId = concertId
        self.purchased = purchased
        self.confirmationCode = confimationCode
