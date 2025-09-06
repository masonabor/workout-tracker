from flask import Blueprint, render_template, g
from app.models import User, Workout

account_view_bp = Blueprint('account_view', __name__, url_prefix='/account')


@account_view_bp.route('/homepage')
def homepage() -> str:
    user_id = g.user.id
    if not user_id:
        abort(404)
    workouts = Workout.query.filter_by(user_id=user_id).all() # передавати як іменоватий аргумент, тобто user_id=user_id, бо в kwargs не можна знайти аргумент, якщо він не іменований
    return render_template('homepage.html', workouts=workouts)


@account_view_bp.route('/register')
def register() -> str:
    return render_template('register.html')