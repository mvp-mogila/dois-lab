from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from database.sql_provider import SQLProvider
from database.connection import DBContextManager, db_config


auth_app = Blueprint('auth_app', __name__, template_folder = "templates")
sql_provider = SQLProvider('sql')
database = DBContextManager(db_config)


@auth_app.route('/')
def auth_handler():
    user_not_found = False
    with database as cursor:
        if cursor:
            login = request.args.get('login')
            password = request.args.get('pass')
            if (login and password):
                params = {"login": login, "password": password}
                sql_code = sql_provider.get_sql('get_user_by_pass.sql', params)
                rows_count = cursor.execute(sql_code)
                if (not rows_count):
                    user_not_found = True
                else:
                    user_data = cursor.fetchone()
                    session['user_login'] = user_data["user_login"]
                    session['user_group'] = user_data["user_group"]
                    session.modified = True
                    return redirect('/')
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return render_template('auth.html', user_not_found = user_not_found, user_login = login)


@auth_app.route('/sign-up', methods = ['GET', 'POST'])
def signup_handler():
    user_found = False
    user_created = False
    if request.method == 'POST':
        with database as cursor:
            if cursor:
                login = request.form.get('login')
                password = request.form.get('pass')
                params = {"login": login, "password": password}
                sql_code = sql_provider.get_sql('check_user.sql', params)
                rows_count = cursor.execute(sql_code)
                if (not rows_count):
                    sql_code = sql_provider.get_sql('add_extern_user.sql', params)
                    rows_count = cursor.execute(sql_code)
                    if (rows_count != 1):
                        raise ValueError("ERROR. INSERTION CANCELLED!")
                    user_created = True
                else:
                    user_found = True
            else:
                raise ValueError("ERROR. CURSOR NOT CREATED!")
    return render_template('sign-up.html', user_found = user_found, user_created = user_created)