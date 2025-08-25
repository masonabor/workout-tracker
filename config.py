import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'ovnksorjivoskodnv' # for development included
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://user:password@localhost/workout'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # параметр, якщо True, то SQLAlchemy слухає всі зміни в моделях (об'єктах) та дозволяє реагувати на такі зміни