from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, username, password, role, pinkey):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None
        

def init_db():
    db.drop_all()
    db.create_all()
    new_user1 = User(username='admin', email='admin@test.com', password='password', role="admin")
    new_user2 = User(username='user', email='user@test.com', password='password', role="user")
    new_user3 = User(username='venue', email='venue@test.com', password='password', role='venue')
    db.session.add(new_user1)
    db.session.add(new_user2)
    db.session.add(new_user3)
    db.session.commit()
init_db()