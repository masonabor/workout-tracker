from .render.account import account_bp
from .render.auth import auth_bp
from .render.workouts import workouts_bp
from .view.account_view import account_view_bp
from .view.workouts_view import workouts_view_bp
from .view.home import home_bp
from .view.auth_view import auth_view_bp
from flask import Flask

def register_routes(app: Flask) -> None:
    app.register_blueprint(account_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(account_view_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(workouts_view_bp)
    app.register_blueprint(auth_view_bp)


