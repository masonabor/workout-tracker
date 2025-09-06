from flask import Blueprint, render_template

account_view_bp = Blueprint('account_view', __name__, url_prefix='/account')


@account_view_bp.route('/homepage')
def homepage() -> str:
    return render_temlpate('homepage.html')


@account_view_bp.route('/register')
def register(error: str) -> str:
    return render_template('register.html', error=error)