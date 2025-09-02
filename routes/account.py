from flask import Blueprint, request, render_template, session
from models import User
from database import db
from decorators import login_required
from exceptions import WeekPasswordException

account_bp = Blueprint('account', __name__, url_prefix='/account')


@account_bp.route('/homepage')
@login_required
def homepage() -> str:
    try:
        user = User.query.filter_by(username=session['user']).first()
        return render_template('homepage.html', workouts=user.workouts)
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)


@account_bp.route('/register', methods=['POST', 'GET'])
def register() -> str:
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            return render_template('register.html', error='Заповніть персональні дані')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            return render_template('register.html', error='Користувач з таким логіном або паролем уже існує')

        try:
            check_password(password)
            db.session.add(User(username, email, password))
            db.session.commit()
            session['user'] = username
            session['id'] = User.query.filter_by(username=username).first().id
            return render_template('homepage.html')
        except WeekPasswordException as e:
            print(e)
            return render_template('register.html', error=e)
        except Exception as e:
            print(e)
            return render_template('error.html', error=e)
    return render_template('register.html')


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


