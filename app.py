from flask import Flask
from config import Config
from routes import auth_bp # через назваПапки.файл імпортуємо компонент з іншої папки
from routes import account_bp
from routes import workouts_bp
from database import db

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)