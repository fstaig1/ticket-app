from website import db
from website.models import User, Artist, Venue, Concert

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
                                ))
        db.session.commit()
    
    with open("data\\venues.txt", "r") as file:
        for line in file:
            data = line.split("\n")[0].split(",")
            db.session.add(Venue(name=str(data[0]),
                                 location=str(data[1]), 
                                 capacity=int(data[-1])))
        db.session.commit()
    
    