from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from ..models import User, Venue, Artist, Concert
from main import requires_roles
from .forms import CreateUserForm, CreateVenueForm
from .. import db

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    global createUserForm
    global createVenueForm
    createUserForm = CreateUserForm()
    createVenueForm = CreateVenueForm()
    return render_template('admin.html', createUserForm=createUserForm, createVenueForm=createVenueForm)


@admin_blueprint.route('/admin/view_all_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
    return render_template('admin.html', current_users=User.query.all(), createUserForm=createUserForm, createVenueForm=createVenueForm)


@admin_blueprint.route('/admin/view_all_venues', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_venues():
    return render_template('admin.html', venues=Venue.query.all(), createUserForm=createUserForm, createVenueForm=createVenueForm)


@admin_blueprint.route('/admin/view_all_artists', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_artists():
    return render_template('admin.html', artists=Artist.query.all(), createUserForm=createUserForm, createVenueForm=createVenueForm)


@admin_blueprint.route('/admin/view_all_concerts', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_concerts():
    return render_template('admin.html', concerts=Concert.query.all(), createUserForm=createUserForm, createVenueForm=createVenueForm)


@admin_blueprint.route('/admin/delete_user', methods=['POST'])
@login_required
@requires_roles('admin')
def delete_user():
    user = User.query.filter_by(id=request.form.get("remove_button")).first()
    user.delete()
    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/admin/create_user', methods=['POST'])
@login_required
@requires_roles('admin')
def create_user():
    createUserForm = CreateUserForm()
    if createUserForm.validate_on_submit():
        if createUserForm.venueId.data:
            venueManager = True
        else:
            venueManager = False

        newUser = User(firstname=createUserForm.firstname.data,
                       lastname=createUserForm.lastname.data,
                       email=createUserForm.email.data,
                       password=createUserForm.password.data,
                       role=createUserForm.role.data,
                       venueManager=venueManager,
                       venueId=createUserForm.venueId.data)

        db.session.add(newUser)
        db.session.commit()
    else:
        for i in createUserForm.errors:
            flash(f'{i}')
    return redirect(url_for('admin.admin'))


@admin_blueprint.route('/admin/create_venue', methods=['POST'])
@login_required
@requires_roles('admin')
def create_venue():
    createVenueForm = CreateVenueForm()
    if createVenueForm.validate_on_submit():
        newVenue = Venue(name=createVenueForm.name.data,
                         location=createVenueForm.location.data,
                         capacity=createVenueForm.capacity.data)
        db.session.add(newVenue)
        db.session.commit()
    else:
        for i in createUserForm.errors:
            flash(f'{i}')
    return redirect(url_for('admin.admin'))
