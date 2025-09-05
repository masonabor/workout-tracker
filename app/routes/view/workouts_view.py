from flask import Blueprint, render_template
from app.models import Workout, Exercise

workouts_view_bp = Blueprint('workouts_view', __name__, url_prefix='/workouts')


@workouts_view_bp.route('/view')
def workouts_view(workout: Workout) -> str:
    return render_template('workouts_details.html', workout=workout)


@workouts_view_bp.route('createWorkout')
def create_workout_view() -> str:
    return render_template('create_workout.html')


@workouts_view_bp.route('/addExercise')
def add_exercise(workout: Workout) -> str:
    return render_template('add_exercise.html', workout_id=workout.id)