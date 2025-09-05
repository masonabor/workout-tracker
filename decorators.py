from functools import wraps
from flask import session, render_template
from models import Base

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return func(*args, **kwargs)
        else:
            return render_template('login.html', error='Для доступу потрібно авторизуватися')
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return render_template('error.html', error='Ви не є адміністратором')
    return wrapper


def owner_required(model: Base, param: str): # ось тут знаходиться параметр, який приймає декоратор
    """
    Декоратор приймає модель (Workout, Exercise etc.) та id, шукає через query об'єкт та повертає цей об'єкт,
    для реалізації потрібно було створити методи get_user() в моделях.
    Також тепер це є "декоратор фабрика", тому що по суті декоратор всередині owner_required,
    проте є можливість приймати параметр в декораторі owner_required.
    Також продемонстровано використання kwargs
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model_id = kwargs.pop(param) # використовуємо pop() щоб дістати та одразу видалити ключ, бо в kwargs він залишається аж до виклику func(), яка приймає тільки один аргумент, якщо не видалити, то буде два параметри: param та model_obj (помилка TypeError)
            if not model_id:
                abort(400)

            model_obj = model.query.get_or_404(model_id)
            if model_obj.get_user().id != session.get('id'): # краще використовувати get, тоді не буде KeyError
                abort(403)

            return func(model_obj, *args, **kwargs)
        return wrapper
    return decorator