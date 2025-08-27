from functools import wraps
from flask import session, render_template

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return func(*args, **kwargs)
        else:
            return render_template('login.html', error='Для доступу потрібно авторизуватися')
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return render_template('error.html', error='Ви не є адміністратором')
    return wrapper