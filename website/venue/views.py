from flask import render_template, Blueprint

venue_blueprint = Blueprint('venue', __name__, template_folder='templates')

@venue_blueprint.route('/venue')
def venue():
    return render_template('venue.html')
