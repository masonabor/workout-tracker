from flask import Flask
from app.config import Config
from app.routes import auth_bp # через назваПапки.файл імпортуємо компонент з іншої папки
from app.routes import account_bp
from app.routes import workouts_bp
from app.routes import home_bp
from app.extensions import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize of DB
    # application factory pattern
    db.init_app(app) # метод для ініціалізації підключення до БД (якщо об'єкт бд знаходиться в іншому файлі)

    # register of blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()

    return app