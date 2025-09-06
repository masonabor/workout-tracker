from flask import Blueprint, request, session, redirect, url_for, Response, flash
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # blueprint як підпрограма, яка потім в основному файлі підключається до основного застосунку


@auth_bp.route('/login', methods=['POST'])
def login() -> Response:
    identifier = request.form['identifier'].strip()
    password = request.form['password']

    existing_user = User.query.filter((User.username==identifier) | (User.email==identifier)).first()

    if existing_user:
        if not existing_user.check_password(password):
            flash('Неправильний пароль', 'danger') # дозволяє зберегти одноразове повідомлення в сесії користувача, зберігається в session['_flashes'], існує до наступного http запиту (get_flashed_messages на вбюшці)
            return redirect(url_for('auth.login'))
        session['user'] = existing_user.username
        session['id'] = existing_user.id
    else:
        flash('Користувача не знайдено', 'danger')
        return redirect(url_for('auth.login'))
    flash(existiong_user.workouts)
    return redirect(url_for('account.homepage'))


@auth_bp.route('/logout')
def logout() -> Response:
    if session.get('user'):
        session.pop('user')
        session.pop('id')
        return redirect(url_for('home.home'))
    else:
        return redirect(url_for('auth.login'))