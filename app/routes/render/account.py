from flask import Blueprint, request, render_template, session, redirect, url_for, Response
from app.models import User
from app.extensions import db
from app.decorators import login_required
from app.exceptions import WeekPasswordException

account_bp = Blueprint('account', __name__, url_prefix='/account')


@account_bp.route('/register', methods=['POST'])
def register() -> Response | None:
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not username or not email or not password:
        return redirect(url_for('account.register', error='Заповніть персональні дані'))

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

    if existing_user:
        return redirect(url_for('account.register', error='Заповніть персональні дані'))

    try:
        check_password(password)
        db.session.add(User(username, email, password))
        db.session.commit()
        session['user'] = username
        session['id'] = User.query.filter_by(username=username).first().id
        return redirect(url_for('home.homepage'))
    except WeekPasswordException as e:
        print(e)
        abort(404)
    except Exception as e:
        print(e)
        abort(404)


def check_password(password: str) -> bool:
    if len(password) < 8:
        raise WeekPasswordException('Пароль повинен бути принаймі 8 символів')
    spec_symb = '!@#$%^&*()/|\\~`<>,.?;:'
    spec_symb_list = {char for char in spec_symb}
    if not bool(set(password).intersection(spec_symb_list)):
        raise WeekPasswordException('Для безпеки потрібно додати спеціальні символи')
    if password == password.lower():
        raise WeekPasswordException('Для безпеки потрібно додати принаймі одну букву у великому регістрі')

    return True


