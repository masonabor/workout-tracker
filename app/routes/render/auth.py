from flask import Blueprint, request, session, redirect, url_for, Response
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # blueprint як підпрограма, яка потім в основному файлі підключається до основного застосунку


@auth_bp.route('/login', methods=['POST'])
def login() -> Response:
    identifier = request.form['identifier']
    password = request.form['password']

    existing_user = User.query.filter((User.username==identifier) | (User.email==identifier)).first()

    if existing_user:
        if not existing_user.check_password(password):
            return redirect(url_for('auth.login', error='Неправильний пароль'))
        session['user'] = existing_user.username
        session['id'] = existing_user.id
    else:
        return redirect(url_for('auth.login', error='Користувача з таким логіном не знайдено'))
    return redirect(url_for('account.homepage'))


@auth_bp.route('/logout')
def logout() -> Response:
    if session.get('user'):
        session.pop('user')
        session.pop('id')
        return redirect(url_for('home.home'))
    else:
        return redirect(url_for('auth.login'))