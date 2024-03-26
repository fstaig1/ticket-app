from flask import render_template, Blueprint
from flask_login import login_required
from ..models import User, Venue, Artist, Concert
from main import requires_roles

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')


@admin_blueprint.route('/view_all_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
    return render_template('admin.html', current_users=User.query.all())


@admin_blueprint.route('/view_all_venues', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_venues():
    return render_template('admin.html', venues=Venue.query.all())


@admin_blueprint.route('/view_all_artists', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_artists():
    return render_template('admin.html', artists=Artist.query.all())


@admin_blueprint.route('/view_all_concerts', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_concerts():
    return render_template('admin.html', concerts=Concert.query.all())
