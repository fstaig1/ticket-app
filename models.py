from app import db, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, email, password, role):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None
        

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(email='admin@test.com', password='Password1!', role="admin"))
    db.session.add(User(email='user@test.com', password='Password1!', role="user"))
    db.session.add(User( email='venue@test.com', password='Password1!', role='venue'))
    db.session.commit()
    
if __name__ == '__main__':
    with app.app_context():
        init_db()