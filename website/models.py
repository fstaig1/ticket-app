from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, firstname, lastname, email, password, role):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None

  
class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    concerts = db.relationship('Concert', backref='artists')
    
    def __init__(self, name):
        self.name = name


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    concerts = db.relationship('Concert', backref='venues')
    
    def __init__(self, name, location, capacity):
        self.name = name
        self.location = location
        self.capacity = capacity
    
    
class Concert(db.Model):
    __tablename__ = 'concerts'
    id = db.Column(db.Integer, primary_key=True)
    
    artistId = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artistName = db.Column(db.String(100), nullable=False)
    
    venueid = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venueName = db.Column(db.String(100), nullable=False)
    
    ticketPrice = db.Column(db.Float, nullable=False)
    
    def __init__(self, artistId, artistName, venueId, venueName, ticketPrice):
        self.artistId = artistId
        self.artistName = artistName 
        self.venueId = venueId
        self.venueName = venueName
        self.ticketPrice = ticketPrice