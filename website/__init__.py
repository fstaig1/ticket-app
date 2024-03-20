from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy() 
def app():

  
    app = Flask(__name__, instance_path="/instance")
    app.config['SECRET_KEY'] = '6LfaX9ocAAAAABWeVBjjXEZTI5tmcxVkO0fDi32J'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    db.init_app(app=app)
    
    
    
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from .models import User


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app