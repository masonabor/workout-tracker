# файл для створення пакету, назва пакету - це назва папки (не потрібно прописувати routes.auth і так далі)
from .auth import auth_bp
from .account import account_bp
from .workouts import workouts_bp
from .home import home_bp