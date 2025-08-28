from flask import Blueprint, request, render_template, session
from models import User, Workout
from database import db
from datetime import datetime

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


@workouts_bp.route('/view/<workout_id>')
def workouts_view(workout_id: int):
    try:
        workout = Workout.query.get(workout_id)

        if workout.user_id != session['id']:
            return render_template('error.html', error='Ви не є власником цього тренування')

    except Exception as e:
        print(e)
        return render_template('error.html', error=e)
    return render_template('workout_details.html', workout=workout)


@workouts_bp.route('/createWorkout', methods=['GET', 'POST'])
def create_workout():
    if request.method == 'GET':
        return render_template('create_workout.html')

    name = request.form['name']
    date = request.form['date']
    user = User.query.filter_by(username=session['user']).first()

    if not name and not date:
        return render_template('create_workout.html', error='Потрібно заповнити усі поля')

    if not user:
        return render_template('error.html', error='Користувач незареєстрований')

    parsed_date = datetime.strptime(date, '%Y-%m-%d')

    try:
        db.session.add(Workout(name, parsed_date, user))
        db.session.commit()
        return render_template('homepage.html', workouts=user.workouts)
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)