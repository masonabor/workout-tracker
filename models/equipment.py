from .base import Base
from database import db
from .exercise import Exercise

class Equipment(Base):
    __tablename__ = 'equipments'

    name = db.Column(db.String(60), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    exercise = db.relationship('Exercise', back_populates='equipments', lazy='selectin')
    sets = db.relationship('Set', back_populates='equipment', lazy='selectin')

    def __init__(self,
                 name: str,
                 exercise: Exercise = None,
                 exercise_id: int = None) -> None:

        self.name = name

        if exercise_id:
            self.exercise_id = exercise_id
        elif exercise:
            self.exercise = exercise
        else:
            raise ValueError('Machine має бути пов\'язаним з exercise')


    def get_user(self) -> 'User':
        return self.exercise.get_user()