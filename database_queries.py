from database import db_session
from models import User, Film


def get_new_films():
    new_films = db_session.query(Film).order_by(Film.added_info).limit(20).all()
    return new_films


def get_users():
    users = db_session.query(User).all()
    return users
