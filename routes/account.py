from flask import Blueprint, request, render_template, url_for, session
from models import User, Workout
from database import db

account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route('/test')
def test() -> str:
    return render_template('base.html')


@account_bp.route('/homepage')
def homepage():
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
            return render_template('base.html', error='Користувач з таким логіном або паролем уже існує')

        db.session.add(User(username, email, password))
        db.session.commit()
        return render_template('base.html')
    return render_template('register.html')

