from .base import Base
from database import db
from datetime import datetime
from .equipment import Equipment

class Set(Base):
    __tablename__ = 'sets'

    machine_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    equipment = db.relationship('Equipment', back_populates='sets', lazy='selectin')
    count = db.Column(db.Integer)
    rest_time = db.Column(db.DateTime)

    def __init__(self,
                 count: int,
                 rest_time: datetime,
                 equipment: Equipment = None,
                 equipment_id: int = None) -> None:

        self.count = count
        self.rest_time = rest_time
        if equipment_id:
            self.machine_id = equipment_id
        elif equipment:
            self.equipment = equipment
        else:
            raise ValueError('Set має бути пов\'язаним з machine')