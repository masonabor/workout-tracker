from database import db
from .base import Base

class Workout(Base):
    __tablename__ = 'workouts'


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
