from . import db
from .models import User, Artist, Venue, Concert  # noqa: F401
from random import randint
from datetime import datetime


def init_db():
    """Method to create test data from files.

    Path: test_data\\*"""

    print(
        """
          Initialising Database ...
          """
    )

    db.drop_all()
    db.create_all()

    # create all artists from file
    with open("test_data\\artists.txt", "r") as file:
        for line in file:
            db.session.add(Artist(name=str(line.split("\n")[0])))

        db.session.commit()

    # create all users from file
    with open("test_data\\users.txt", "r") as file:
        for line in file:
            data = line.split("\n")[0].split(",")

            if data[5] == "":
                data[5] = None

            db.session.add(
                User(
                    firstname=str(data[0]),
                    lastname=str(data[1]),
                    email=str(data[2]),
                    password=str(data[3]),
                    role=str(data[4]),
                    venueId=data[5],
                )
            )

        db.session.commit()

    # create all venues from file
    with open("test_data\\venues.txt", "r") as file:
        for line in file:
            data = line.split("\n")[0].split(",")

            db.session.add(
                Venue(name=str(data[0]), location=str(data[1]), capacity=int(data[-1]))
            )

        db.session.commit()

    artists = Artist.query.all()
    venues = Venue.query.all()

    # create concerts + tickets
    for i in range(10):
        # create 10 concerts for wembley stadium with limited capacity for testing
        artist = artists[randint(1, len(artists) - 1)]

        concert = venues[0].create_Concert(
            artistId=artist.id,
            artistName=artist.name,
            ticketPrice=randint(10, 100),
            date=datetime(2025, randint(1, 12), randint(1, 28), 19),
            availableTickets=i + 1,
        )

        ticket = concert.create_ticket(ownerId=randint(1, 3))
        ticket.purchase_ticket()

    for _ in range(10):
        # create 10 pheobe bridgers concerts
        venue = venues[randint(1, len(venues) - 1)]

        concert = venue.create_Concert(
            artistId=artists[2187].id,
            artistName=artists[2187].name,
            ticketPrice=randint(10, 100),
            date=datetime(2025, randint(1, 12), randint(1, 28), 19),
            availableTickets=randint(0, venue.capacity),
        )

        ticket = concert.create_ticket(ownerId=randint(1, 3))
        ticket.purchase_ticket()

    for _ in range(50):
        # create 50 random concerts
        artist = artists[randint(1, len(artists) - 1)]
        venue = venues[randint(1, len(venues) - 1)]

        concert = venue.create_Concert(
            artistId=artist.id,
            artistName=artist.name,
            ticketPrice=randint(10, 100),
            date=datetime(2025, randint(1, 12), randint(1, 28), 19),
            availableTickets=randint(0, venue.capacity),
        )

        ticket = concert.create_ticket(ownerId=randint(1, 3))
        ticket.purchase_ticket()

    print(
        """
          Finished!
          """
    )
