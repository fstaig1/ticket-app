from flask import render_template
from ..views import venue_blueprint


@venue_blueprint.route('/venue')
def venue():
    return render_template('venue.html')
