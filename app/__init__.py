from flask import Flask
from app.config import Config
from app.routes import register_routes
from app.extensions import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize of DB
    # application factory pattern
    db.init_app(app) # метод для ініціалізації підключення до БД (якщо об'єкт бд знаходиться в іншому файлі)

    # register of blueprints
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app