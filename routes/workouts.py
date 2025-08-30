from flask import Blueprint, request, render_template, session, url_for, redirect, Response
from models import User, Workout, Exercise, Set
from database import db
from datetime import datetime, timedelta

from models.equipment import Equipment

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


@workouts_bp.route('/addExercise/<workout_id>', methods=['POST', 'GET'])
def add_exercise(workout_id: int) -> str | Response:
    if request.method == 'GET':
        return render_template('add_exercise.html', workout_id=workout_id)

    user = User.query.filter_by(username=session['user']).first()
    if not user:
        return render_template('error.html', error='Ви не ввійшли')

    workout = user.workouts[int(workout_id)-1]

    if not workout:
        return render_template('error.html', error='Тренування з таким id у даного користувача не знайдено')

    name = request.form['name']
    equipment = request.form['equipment']

    if not name:
        return render_template('add_exercise.html', error='Введіть назву вправи')

    try:
        exercise = Exercise(name, workout)
        db.session.add(exercise)
        if equipment:
            db.session.add(Equipment(equipment, exercise))
        db.session.commit()
        return redirect(url_for('workouts.workouts_view', workout_id=workout_id))
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)


@workouts_bp.route('/addEquipment/<exercise_id>', methods=['POST'])
def add_equipment(exercise_id: int) -> str:
    user = Exercise.query.filter_by(id=exercise_id).first().workout.user
    if user.id != session['id']:
        return render_template('error.html', error='Ви не є власником вправи')

    name = request.form['name']
    if not name:
        return render_template('error.html', error='Введіть назву устаткування')

    try:
        db.session.add(Equipment(name, exercise_id=exercise_id))
        db.session.commit()
        exercise = Exercise.query.get(exercise_id)
        return render_template('workout_details.html', workout=exercise.workout)
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)


@workouts_bp.route('/addSets/<equipment_id>', methods=['POST'])
def add_sets(equipment_id: int) -> str:
    equipment = Equipment.query.get(equipment_id)
    user = equipment.exercise.workout.user
    if user.id != session['id']:
        return render_template('error.html', error='Ви не є власником тренування')

    count = int(request.form['count'])
    print(request.form['rest_time'])

    rest_time = datetime.strptime(request.form['rest_time'], '%H:%M:%S')
    if not count:
        return render_template('error.html', error='')

    try:
        db.session.add(Set(count, rest_time, equipment))
        db.session.commit()
        return render_template('workout_details.html', workout=equipment.exercise.workout)
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)