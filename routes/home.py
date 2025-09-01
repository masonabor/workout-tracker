from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@home_bp.route('/home')
def home():
    return render_template('main.html', session=session)