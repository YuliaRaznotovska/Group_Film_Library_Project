import functools

from dateutil import parser
from flask import Flask, url_for
from flask import request, render_template, session, redirect
from sqlalchemy import select, desc, or_

import database
import models

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def decorator_check_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('get_user_login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def main_page():
    database.init_db()
    result = database.db_session.execute(
        select(models.Film).order_by(desc(models.Film.added_info)).limit(10)).scalars().all()
    actors = database.db_session.execute(select(models.Actor, models.ActorFilm).join(models.ActorFilm,
                                                                                     models.Actor.id == models.ActorFilm.actor_id)).all()
    genres = database.db_session.execute(select(models.GenreFilm).join(models.Film,
                                                                       models.GenreFilm.film_id == models.Film.id)).scalars().all()
    return render_template('main.html', films=result, actors=actors, genres=genres)


@app.route('/register', methods=['GET'])
def get_user_registration():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def complete_user_registration():
    first_name = request.form["user_first_name"]
    last_name = request.form["user_last_name"]
    password = request.form["password"]
    login = request.form["login"]
    email = request.form["user_email"]
    phone_number = request.form["user_phone_num"]
    birth_date = parser.parse(request.form["user_birth_date"])
    database.init_db()
    new_user = models.User(first_name=first_name, last_name=last_name, password=password, login=login, email=email,
                           phone_number=phone_number, birth_date=birth_date)
    database.db_session.add(new_user)
    database.db_session.commit()
    return 'Registered'


@app.route('/login', methods=['GET'])
def get_user_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def complete_user_login():
    login = request.form['login']
    password = request.form['password']
    database.init_db()
    user = database.db_session.execute(select(models.User).where(models.User.login == login)).scalar_one_or_none()
    if user is None:
        return 'User is not found'
    if user.password != password:
        return 'Incorrect password'
    else:
        session['logged_in'] = True
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        return f'Welcome {session["first_name"]} {session["last_name"]}! You are logged in.'


@app.route('/logout', methods=['GET'])
@decorator_check_login
def user_logout():
    session.clear()
    return "Logged out"


@app.route('/users/<user_id>', methods=['GET'])
def get_user_id(user_id):
    database.init_db()
    user_by_session = session.get('user_id')
    user_by_id = database.db_session.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if user_by_session is not None:
        user_by_session = database.db_session.execute(
            select(models.User).where(models.User.id == user_by_session)).scalar_one_or_none()
    return render_template('user_page.html', user=user_by_id, user_session=user_by_session)


@app.route('/users/<user_id>', methods=['POST'])
def update_user_id_profile(user_id):
    database.init_db()
    session_user_id = session.get('user_id')
    if int(user_id) != session_user_id:
        return 'You can edit only your profile'
    else:
        first_name = request.form["user_first_name"]
        last_name = request.form["user_last_name"]
        password = request.form["password"]
        email = request.form["user_email"]
        phone_number = request.form["user_phone_num"]
        birth_date = parser.parse(request.form["user_birth_date"])
        additional_info = request.form["user_additional_info"]
        user = database.db_session.execute(
            select(models.User).where(models.User.id == session_user_id)).scalar_one_or_none()
        if user is not None:
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            user.email = email
            user.phone_number = phone_number
            user.birth_date = birth_date
            user.additional_info = additional_info
            database.db_session.commit()
    return f'User {user_id} updated'


@app.route('/users/<user_id>/delete', methods=['GET'])
@decorator_check_login
def delete_user_id(user_id):
    session_user_id = session.get('user_id')
    if session_user_id == user_id:
        return f'User {user_id} deleted'
    else:
        return f'You can delete only your profile'


@app.route('/films', methods=['GET'])
def get_film_list():
    database.init_db()
    filter_params = request.args
    films_query = select(models.Film).distinct()
    for key, value in filter_params.items():
        if value:
            if key == 'name':
                films_query = films_query.where(models.Film.name.ilike(f'%{value}%'))
            elif key == 'genre':
                films_query = films_query.join(models.Film.genres).where(
                    models.Genre.genre.ilike(f'%{value}%'))
            elif key == 'actor_name':
                films_query = films_query.join(models.Film.actors).where(
                    or_(models.Actor.actor_first_name.ilike(f'%{value}%'),
                        models.Actor.actor_last_name.ilike(f'%{value}%')))
            elif key == 'country':
                films_query = films_query.join(models.Film.country_selection).where(
                        models.Country.country_name.like(f'%{value}%'))
            elif key == 'year':
                films_query = films_query.where(models.Film.year == value)
            elif key == 'rating':
                films_query = films_query.where(models.Film.rating == value)
    result = database.db_session.execute(films_query).scalars().all()
    genres = database.db_session.execute(select(models.Genre).order_by(models.Genre.genre)).scalars().all()
    actors = database.db_session.execute(select(models.Actor).join(models.Actor.films)).scalars().all()
    countries = database.db_session.execute(
        select(models.Country).order_by(models.Country.country_name)).scalars().all()
    return render_template('films.html', films=result, genres=genres, actors=actors, countries=countries)


@app.route('/films/add', methods=['GET'])
@decorator_check_login
def add_film_profile():
    database.init_db()
    user_session = session.get('user_id')
    if not user_session:
        return 'You can not add film'
    else:
        user_session = database.db_session.execute(
            select(models.User).where(models.User.id == user_session)).scalar_one_or_none()
        return render_template('add_film_profile.html', user_session=user_session)


@app.route('/films/add', methods=['POST'])
@decorator_check_login
def add_film_complete():
    database.init_db()
    session_user_id = session.get('user_id')
    if not session_user_id:
        return 'You can not add film'
    else:
        name = request.form["name"]
        year = request.form["year"]
        poster = request.form["poster"]
        description = request.form["description"]
        rating = request.form["rating"]
        duration = request.form["duration"]
        country = request.form["country"]
        added_info = request.form["added_info"]

        new_film = models.Film(name=name, year=year, poster=poster, description=description, rating=rating,
                               duration=duration, country=country, added_info=added_info)
        country_obj = database.db_session.execute(
            select(models.Country).where(models.Country.country_name == country)).scalar_one_or_none()
        if not country_obj:
            country_obj = models.Country(country_name=country)
            database.db_session.add(country_obj)
        new_film.country = country_obj.country_name

        genre_input = request.form["genres"]
        genre_names = [genre.strip() for genre in genre_input.split(",") if genre.strip()]
        for name in genre_names:
            genre_obj = database.db_session.execute(
                select(models.Genre).where(models.Genre.genre == name)).scalar_one_or_none()
            if not genre_obj:
                genre_obj = models.Genre(genre=name)
                database.db_session.add(genre_obj)
            new_film.genres.append(genre_obj)

        actor_first_name_input = request.form["actor_first_name"]
        actor_last_name_input = request.form["actor_last_name"]
        actors_first_names = [actor.strip() for actor in actor_first_name_input.split(",")
                              if actor_first_name_input.strip()]
        actors_last_names = [actor.strip() for actor in actor_last_name_input.split(",") if
                             actor_last_name_input.strip()]
        for first_name, last_name in zip(actors_first_names, actors_last_names):
            actor_obj = database.db_session.execute(select(models.Actor).where(
                models.Actor.actor_first_name == first_name,
                models.Actor.actor_last_name == last_name)).scalar_one_or_none()
            if not actor_obj:
                actor_obj = models.Actor(actor_first_name=first_name, actor_last_name=last_name)
                database.db_session.add(actor_obj)
            new_film.actors.append(actor_obj)
        database.db_session.add(new_film)
        database.db_session.commit()
    return 'New film added'


@app.route('/films/<film_id>', methods=['GET'])
def get_film(film_id):
    result = database.db_session.execute(select(models.Film).where(models.Film.id == film_id)).scalars().all()
    actors = database.db_session.execute(select(models.Actor).join(models.ActorFilm,
                                                                   models.Actor.id == models.ActorFilm.actor_id)
                                         .where(models.ActorFilm.film_id == film_id)).scalars().all()
    genres = database.db_session.execute(
        select(models.GenreFilm).where(models.GenreFilm.film_id == film_id)).scalars().all()
    return render_template('film_profile.html', film_list=result, actors=actors, genres=genres)


@app.route('/films/update/<film_id>', methods=['POST'])
@decorator_check_login
def update_film(film_id):
    return render_template('film_update.html')


@app.route('/films/<film_id>', methods=['DELETE'])
@decorator_check_login
def delete_film(film_id):
    return f'Film {film_id} deleted'


@app.route('/films/<film_id>/rating', methods=['GET'])
def get_rating(film_id):
    film = database.db_session.execute(select(models.Film).where(models.Film.id == film_id)).scalar_one_or_none()
    return f'Film {film.name} has rating {film.rating}'


@app.route('/films/<film_id>/rating', methods=['POST'])
@decorator_check_login
def post_rating(film_id):
    return f'Film {film_id} rated'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['GET'])
def get_feedback(film_id, feedback_id):
    return f'Film {film_id} is rated {feedback_id}'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['DELETE'])
@decorator_check_login
def delete_feedback(film_id, feedback_id):
    return f'Film {film_id} feedback {feedback_id} deleted'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['PUT'])
@decorator_check_login
def update_feedback(film_id, feedback_id):
    return f'Film {film_id} feedback is {feedback_id}'


@app.route('/films/<film_id>/rating/<feedback_id>/feedback', methods=['GET'])
def get_feedback_description(film_id, feedback_id):
    film = database.db_session.execute(select(models.Film).where(models.Film.id == film_id)).scalar_one_or_none()
    feedback = database.db_session.execute(select(models.Feedback).where(models.Feedback.film_id == film_id,
                                                                         models.Feedback.id == feedback_id)).scalar_one_or_none()
    return f'Film {film.name} has the following feedback: {feedback.description}'


@app.route('/users/<user_id>/lists', methods=['GET'])
def get_user_lists(user_id):
    return f'{user_id} Lists'


@app.route('/users/<user_id>/lists', methods=['POST'])
@decorator_check_login
def add_list(user_id):
    return f'{user_id} New List'


@app.route('/users/<user_id>/lists/<list_id>', methods=['DELETE'])
@decorator_check_login
def delete_user_list(user_id, list_id):
    return f'{user_id} list {list_id} deleted'


@app.route('/users/<user_id>/lists/<list_id>', methods=['GET'])
def get_watch_later_list(user_id, list_id):
    return f'{user_id} wants to watch {list_id} '


@app.route('/users/<user_id>/lists/<list_id>/<film_id>', methods=['POST'])
@decorator_check_login
def add_film_to_watch_list(user_id, list_id, film_id):
    return f'{user_id} added {film_id} to the list {list_id}'


@app.route('/users/<user_id>/lists/<list_id>/<film_id>', methods=['DELETE'])
@decorator_check_login
def delete_film_from_watch_list(user_id, list_id, film_id):
    return f'{user_id} deleted {film_id} from the list {list_id}'


@app.route('/actor/<actor_id>', methods=['GET'])
def get_actor(actor_id):
    actor = database.db_session.execute(select(models.Actor).where(models.Actor.id == actor_id)).scalar_one_or_none()
    films = database.db_session.execute(select(models.Film)
                                        .join(models.ActorFilm, models.ActorFilm.film_id == models.Film.id)
                                        .where(models.ActorFilm.actor_id == actor_id)).scalars().all()
    return render_template("actor_profile.html", actor=actor, films=films)


if __name__ == '__main__':
    app.run()
