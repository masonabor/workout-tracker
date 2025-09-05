from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__, url_prefix='/')


@home_bp.route('/')
@home_bp.route('/home')
def home() -> str:
    return render_template('main.html', session=session)