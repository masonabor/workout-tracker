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
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, username: str, email: str, password:str) -> None:
        self.username = username
        self.email = email
        self.hashed_password = User.hash_password(password)
        self.role = User.ROLE_USER

    @staticmethod
    def hash_password(password: str) -> str:
        # хешування пароля, модуль bcrypt
        # encode() вертає послідовність байтів, де b'' - байти, /x - шістнадцяткове число
        return str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()))

    @staticmethod
    def create_admin(username: str, email: str, password: str) -> 'User':
        user = User(username, email, password)
        user.role = User.ROLE_ADMIN
        return user