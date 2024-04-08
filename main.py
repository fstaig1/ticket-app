from website import app
from functools import wraps
from flask import render_template, abort
from flask_login import LoginManager, current_user
from website.initdb import init_db  # noqa: F401
from website.models import User
from werkzeug.exceptions import HTTPException

# app config from __init__.py
app = app()


# enforces that a user has a role before accessing a page
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return abort(403, "Forbidden")
            return f(*args, **kwargs)

        return wrapped

    return wrapper


# routes user to error page
@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template("error.html", error=e)


# routes user to homepage
@app.route("/")
def index():
    return render_template("index.html")


# starts app
if __name__ == "__main__":
    login_manager = LoginManager()
    login_manager.login_view = "users.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from website.users.views import users_blueprint
    from website.admin.views import admin_blueprint
    from website.venue.views import venue_blueprint
    from website.shop.views import shop_blueprint
    
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(venue_blueprint)
    app.register_blueprint(shop_blueprint)

    # uncomment this to re initialise the database
    """
    with app.app_context():
        init_db()
    """
    app.run(host="127.0.0.1", port="38255", debug=True)
