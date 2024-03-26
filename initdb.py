from website import db
from website.models import User, Artist, Venue, Concert  # noqa: F401
from random import randint
from datetime import datetime


def init_db():
    db.drop_all()
    db.create_all()

    with open("data\\artists.txt", "r") as file:
        for line in file:
            db.session.add(Artist(name=str(line.split("\n")[0])))
        db.session.commit()

    with open("data\\users.txt", "r") as file:
        for line in file:
            data = line.split("\n")[0].split(",")
            db.session.add(User(firstname=str(data[0]),
                                lastname=str(data[1]),
                                email=str(data[2]),
                                password=str(data[3]),
                                role=str(data[4]),
                                venueManager=bool(data[5]),
                                venueId=data[6],
                                ))
        db.session.commit()

    with open("data\\venues.txt", "r") as file:
        for line in file:
            data = line.split("\n")[0].split(",")
            db.session.add(Venue(name=str(data[0]),
                                 location=str(data[1]),
                                 capacity=int(data[-1])))

        db.session.commit()

    artists = Artist.query.all()
    venues = Venue.query.all()

    for _ in range(10):
        artist = artists[randint(1, len(artists) - 1)]
        venues[0].create_Concert(artistId=artist.id,
                                 artistName=artist.name,
                                 ticketPrice=randint(10, 100),
                                 date=datetime(2025, randint(1, 12), randint(1, 28), 19))

    for _ in range(10):
        venue = venues[randint(1, len(venues) - 1)]
        venue.create_Concert(artistId=artists[2191].id,
                             artistName=artists[2191].name,
                             ticketPrice=randint(10, 100),
                             date=datetime(2025, randint(1, 12), randint(1, 28), 19))

    for _ in range(50):
        artist = artists[randint(1, len(artists) - 1)]
        venue = venues[randint(1, len(venues) - 1)]
        venue.create_Concert(artistId=artist.id,
                             artistName=artist.name,
                             ticketPrice=randint(10, 100),
                             date=datetime(2025, randint(1, 12), randint(1, 28), 19))
