from flask import render_template
from ..views import admin_blueprint


@admin_blueprint.route('/admin')
def admin():
    return render_template('admin.html')
