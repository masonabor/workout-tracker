from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # blueprint як підпрограма, яка потім в основному файлі підключається до основного застосунку

@auth_bp.route('/login')
def get_login_page():
    return render_template('login.html')