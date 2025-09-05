from database import db
from .base import Base
from datetime import datetime
from .user import User

class Workout(Base):
    __tablename__ = 'workouts'

    name = db.Column(db.String(60), nullable=False, default='Workout')
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #двосторонній зв'язок
    exercises = db.relationship('Exercise', backref='workout', lazy='selectin')

    def __init__(self,
                 name: str,
                 date: datetime,
                 user: User = None,
                 user_id: int = None) -> None:

        self.name = name
        self.date = date

        if user:
            self.user = user
        elif user_id:
            self.user_id = user_id
        else:
            raise ValueError('Workout має бути прив\'язаний до користувача')


    def get_user(self) -> 'User':
        return self.user