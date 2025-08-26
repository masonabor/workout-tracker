from flask import Flask
from config import Config
from routes import auth_bp # через назваПапки.файл імпортуємо компонент з іншої папки
from routes import account_bp
from routes import workouts_bp
from database import db

def create_app() -> Flask:
    fapp = Flask(__name__)
    fapp.config.from_object(Config)

    # initialize of DB
    # application factory pattern
    db.init_app(fapp) # метод для ініціалізації підключення до БД (якщо об'єкт бд знаходиться в іншому файлі)

    # register of blueprints
    fapp.register_blueprint(auth_bp)
    fapp.register_blueprint(workouts_bp)
    fapp.register_blueprint(account_bp)

    with fapp.app_context():
        db.create_all()

    return fapp

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)