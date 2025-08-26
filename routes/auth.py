from flask import Blueprint, render_template, request
from models import User
from database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # blueprint як підпрограма, яка потім в основному файлі підключається до основного застосунку


@auth_bp.route('/test')
def test() -> str:
    return render_template('base.html')

@auth_bp.route('/register', methods=['POST', 'GET'])
def register() -> str:
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_users = User.query.filter((User.username == username) or (User.email == email)).first()
        if existing_users:
            return render_template('base.html', error='Username already exists')

        db.session.add(User(username, email, password))
        db.session.commit()
        return render_template('base.html')
    return render_template('register.html')