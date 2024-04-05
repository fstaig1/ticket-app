from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "6LfaX9ocAAAAABWeVBjjXEZTI5tmcxVkO0fDi32J"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticket.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app=app)

    with app.app_context():
        db.create_all()

    return app
