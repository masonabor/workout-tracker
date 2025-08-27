from flask import Blueprint, render_template, request, session, redirect, url_for
from models import User
from .decorators import login_required
from database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # blueprint як підпрограма, яка потім в основному файлі підключається до основного застосунку


@auth_bp.route('/test')
@login_required
def test() -> str:
    return render_template('login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        existing_user = User.query.filter((User.username==identifier) | (User.email==identifier)).first()

        if existing_user:
            check = existing_user.check_password(password)
            if not check:
                return render_template('login.html', error='Неправильний пароль')
            session['user'] = existing_user.username
            session['id'] = existing_user.id
        else:
            return render_template('login.html', error='Користувача з таким логіном не знайдено')
        return redirect(url_for('account.homepage'))
    return render_template('login.html', session=session)


@auth_bp.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('auth.login'))