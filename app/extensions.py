from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # створюємо об'єкт SQLAlchemy без підключення до застосунку

"""
тут lazy initialization - відкладена ініціалізація 
у цьому випадку відклав ініціалізацію підключення до конкретного застосунку, що
дає змогу вільно змінити застосунок на інший.
Можна легко використати цей екземпляр для тестування

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)

engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add(User(username="Alex"))
session.commit()

Цей код приклад використання SQLAlchemy без flask_sqlalchemy
"""

