from flask import Flask
from flask_sqlalchemy import SQLAlchemy




db = SQLAlchemy()  # FIXME i need to init_db somehow this is the worst error ive ever encountered
def app():

  
    app = Flask(__name__, instance_path="/instance")
    app.config['SECRET_KEY'] = '6LfaX9ocAAAAABWeVBjjXEZTI5tmcxVkO0fDi32J'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    db.init_app(app=app)
    return app