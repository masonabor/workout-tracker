from flask import Blueprint, request, render_template, session, url_for, redirect, Response
from models import User, Workout, Exercise, Set
from database import db
from datetime import datetime
from decorators import login_required, owner_required

from models.equipment import Equipment

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


@workouts_bp.route('/view/<int:workout_id>')
@login_required
@owner_required(Workout, param='workout_id')
def workouts_view(workout) -> str:
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


@workouts_bp.route('/addExercise/<int:workout_id>', methods=['POST', 'GET'])
@login_required
@owner_required(Workout, param='workout_id')
def add_exercise(workout) -> str | Response:
    if request.method == 'GET':
        return render_template('add_exercise.html', workout_id=workout.id)

    user = User.query.filter_by(username=session['user']).first()
    if not user:
        return render_template('error.html', error='Ви не ввійшли')

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
        return redirect(url_for('workouts.workouts_view', workout_id=workout.id))
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)


@workouts_bp.route('/addEquipment/<int:exercise_id>', methods=['POST'])
@login_required
@owner_required(Exercise, param='exercise_id')
def add_equipment(exercise) -> str:
    name = request.form['name']
    if not name:
        return render_template('error.html', error='Введіть назву устаткування')

    try:
        db.session.add(Equipment(name, exercise=exercise))
        db.session.commit()
        return render_template('workout_details.html', workout=exercise.workout)
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)


@workouts_bp.route('/addSets/<int:equipment_id>', methods=['POST'])
@login_required
@owner_required(Equipment, param='equipment_id')
def add_sets(equipment) -> str:

    count = int(request.form['count'])
    weight = float(request.form['weight'])
    rest_time = datetime.strptime(request.form['rest_time'], '%H:%M:%S')

    if not count:
        return render_template('error.html', error='Потрібно ввести кількість повторів')

    if not weight:
        return render_template('error.html', error='Потрібно ввести вагу під час підходу')

    try:
        db.session.add(Set(count, weight, rest_time, equipment))
        db.session.commit()
        return render_template('workout_details.html', workout=equipment.exercise.workout)
    except Exception as e:
        print(e)
        return render_template('error.html', error=e)


@workouts_bp.route('/filter')
@login_required
def filter_workouts() -> str:
    """
    Тут треба зрозуміти, що можна отримати query і далі його за потреби фільтрувати, а не писати все в один рядок
    також потрібно використовувати query параметри, так як це зручно, наприклад для фільтрування
    """
    user_id = session['id']
    name = request.args.get('name') # query параметри, передаються ось так: /filter?name=Push&date=2025-08-30, якщо такого параметру немає, то повертає None
    name = name.strip() if name else None
    date_str = request.args.get('date') # request.args зберігає query параметри, які ми передаємо через браузерну строку

    query = Workout.query.filter_by(user_id=user_id)

    if name:
        query = query.filter(Workout.name.ilike(f"%{name}%"))

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Workout.date) == date)
        except ValueError as e:
            print(e)
            return render_template('error.html', error='Невірний формат дати. YYYY-MM-DD')

    workouts = query.order_by(Workout.date.desc()).all()
    return render_template('homepage.html', workouts=workouts)

