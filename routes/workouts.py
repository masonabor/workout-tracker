from flask import Blueprint, request, render_template, session, url_for, redirect, Response
from models import User, Workout, Exercise, Set
from database import db
from datetime import datetime
from decorators import login_required

from models.equipment import Equipment

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


@workouts_bp.route('/view/<workout_id>')
@login_required
def workouts_view(workout_id: int) -> str:
    try:
        workout = Workout.query.get(workout_id)

        if workout.user_id != session['id']:
            return render_template('error.html', error='Ви не є власником цього тренування')

    except Exception as e:
        print(e)
        return render_template('error.html', error=e)
    return render_template('workout_details.html', workout=workout)


@workouts_bp.route('/createWorkout', methods=['GET', 'POST'])
@login_required
def create_workout() -> str:
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
@login_required
def add_exercise(workout_id: int) -> str | Response:
    if request.method == 'GET':
        return render_template('add_exercise.html', workout_id=workout_id)

    user = User.query.filter_by(username=session['user']).first()
    if not user:
        return render_template('error.html', error='Ви не ввійшли')

    workout = Workout.query.get(workout_id)

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
@login_required
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
@login_required
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


@workouts_bp.route('/filter')
@login_required
def filter_workouts() -> str:
    user_id = session['id']
    name = request.args.get('name') # query параметри, передаються ось так: /filter?name=Push&date=2025-08-30, якщо такого параметру немає, то повертає None
    date_str = request.args.get('date') # request.args зберігає query параметри, які ми передаємо через браузерну строку

    query = Workout.query.filter_by(user_id=user_id)

    if name:
        query = query.filter(Workout.name.ilike(f"%{name}%"))

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            query = query.filter(db.func.date(Workout.date) == date)
        except ValueError as e:
            print(e)
            return render_template('error.html', error='Невірний формат дати. YYYY-MM-DD')

    workouts = query.order_by(Workout.date.desc()).all()
    return render_template('homepage.html', workouts=workouts)
"""
Тут треба зрозуміти, що можна отримати query і далі його за потреби фільтрувати, а не писати все в один рядок
також потрібно використовувати query параметри, так як це зручно, наприклад для фільтрування
"""

