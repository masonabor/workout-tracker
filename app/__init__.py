from flask import Flask, session, g
from app.config import Config
from app.routes import register_routes
from app.extensions import db
from app.models import User


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

    @app.before_request # виконається перед буть-яким запитом та додасть у g змінну (g залишається активною протягом одного запиту)
    def load_logged_in_user():
        user_id = session.get('id')
        g.user = User.query.get(user_id) if user_id else None

    return app