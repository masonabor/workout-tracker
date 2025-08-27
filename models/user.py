from database import db
import bcrypt
from .base import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)

    # двосторонній зв'язок
    """
    lazy:
    lazy="select" → дефолт, простий, але може бути повільним.
    lazy="joined" → все тягне одразу JOIN’ом.
    lazy="subquery" → теж одразу, але через підзапит.
    lazy="selectin" → сучасний оптимізований варіант.
    lazy="dynamic" → повертає Query, добре для фільтрації.
    
    backref автоматично створить на іншій стороні зв'язку (тобто Workout), атрибут з користувачем user
    """
    workouts = db.relationship('Workout', lazy='selectin', backref='user')
    role = db.Column(db.String(10), nullable=False)
    date_of_create = db.Column(db.DateTime, default=datetime.now())

    def __init__(self,
                 username: str,
                 email: str,
                 password:str,
                 role: str = ROLE_USER) -> None:

        self.username = username
        self.email = email
        self.hashed_password = User.hash_password(password)
        self.role = role

    @staticmethod
    def hash_password(password: str) -> str:
        # хешування пароля, модуль bcrypt
        # encode() вертає послідовність байтів, де b'' - байти, /x - шістнадцяткове число
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    @classmethod
    def create_admin(cls, username: str, email: str, password: str) -> 'User':
        return cls(username, email, password, role=cls.ROLE_ADMIN)