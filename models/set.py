from .base import Base
from database import db
from datetime import datetime
from .machine import Machine

class Set(Base):
    __tablename__ = 'sets'

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    machine = db.relationship('Machine', back_populates='sets', lazy='selectin')
    count = db.Column(db.Integer)
    rest_time = db.Column(db.DateTime)

    def __init__(self,
                 count: int,
                 rest_time: datetime,
                 machine: Machine = None,
                 machine_id: int = None) -> None:

        self.count = count
        self.rest_time = rest_time
        if machine_id:
            self.machine_id = machine_id
        elif machine:
            self.machine = machine
        else:
            raise ValueError('Set має бути пов\'язаним з machine')