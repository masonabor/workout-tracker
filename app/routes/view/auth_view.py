from flask import Blueprint, render_template

auth_view_bp = Blueprint('auth_view', __name__, url_prefix='/auth')


@auth_view_bp.route('/login')
def login() -> str:
    return render_template('login.html')