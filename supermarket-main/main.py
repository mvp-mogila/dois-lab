#! /bin/python3

from flask import Flask, render_template, session
import os


from catalog.catalog import catalog_app
from auth.auth import auth_app
from internal_users.controller import admin_app
from access.control import login_required, group_required
from report.report import report_app
from basket.basket import basket_app

app = Flask(__name__)
app.register_blueprint(catalog_app, url_prefix='/catalog')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(admin_app)
app.register_blueprint(report_app, url_prefix='/report')
app.register_blueprint(basket_app, url_prefix='/order')

@app.route('/')
def default_handler():
    if (not session.get('basket')):
        session['basket'] = dict()
    user_group = None
    logged = False
    report = False
    if ('user_login' in session):
        logged = True
    if ('user_group' in session):
        user_group = session['user_group']
        report = True
    return render_template('index.html', logged = logged, user_group = user_group, report = report)


@app.route('/client-profile')
@login_required
def client_handler():
    login = session['user_login']
    return render_template('client-profile.html', login = login)


@app.route('/staff-profile')
@group_required
def staff_handler():
    return render_template('staff-profile.html')


if __name__ == '__main__':
    app.secret_key = os.urandom(32)
    app.run(host = '127.0.0.1', port = 5000)
