from .base import Base
from database import db
from .workout import Workout

class Exercise(Base):
    __tablename__ = 'exercises'

    name = db.Column(db.String(60), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    equipments = db.relationship('Equipment', back_populates='exercise', lazy='selectin')

    def __init__(self,
                 name: str,
                 workout: Workout = None,
                 workout_id: int = None) -> None:

        self.name = name

        if workout_id:
            self.workout = workout
        elif workout:
            self.workout = workout
        else:
            raise ValueError('Exercise має бути прив\'язаним до workout')


    def get_user(self) -> 'User':
        return self.workout.get_user()
