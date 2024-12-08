from flask import Blueprint, render_template

from access.control import group_required

admin_app = Blueprint('admin_app', __name__, template_folder = "templates")


@admin_app.route('/stats')
@group_required
def stats_handler():
    return render_template('plug.html')


@admin_app.route('/bills')
@group_required
def bills_handler():
    return render_template('plug.html')


@admin_app.route('/deliveries')
@group_required
def deliveries_handler():
    return render_template('plug.html')


@admin_app.route('/employees')
@group_required
def employees_handler():
    return render_template('plug.html')