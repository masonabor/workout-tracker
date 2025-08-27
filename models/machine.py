from .base import Base
from database import db
from .exercise import Exercise

class Machine(Base):
    __tablename__ = 'machines'

    name = db.Column(db.String(60), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    exercise = db.relationship('Exercise', back_populates='machines', lazy='selectin')
    sets = db.relationship('Set', back_populates='machine', lazy='selectin')

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
