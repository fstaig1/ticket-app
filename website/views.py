from flask import Blueprint, render_template
users_blueprint = Blueprint('users', __name__, template_folder='/templates')
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
venue_blueprint = Blueprint('venue', __name__, template_folder='templates')