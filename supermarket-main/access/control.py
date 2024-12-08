from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from functools import wraps
import json

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if ('user_login' in session):
            return func(*args, **kwargs)
        else:
            return redirect('/auth')
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if ('user_login' in session):
            if (session['user_group']):
                user_group = session.get('user_group')
                user_request = request.url.split('/')
                url = user_request[3]
                with open('access/access_config.json', 'r') as config:
                    config_list = json.load(config)
                    if user_group in config_list:
                        if url in config_list[user_group]:
                            return func(*args, **kwargs)
                        else:
                            return render_template('access-denied.html', client = False)
            else:
                return render_template('access-denied.html', client = True)
        else:
            return redirect('/auth')
    return wrapper
