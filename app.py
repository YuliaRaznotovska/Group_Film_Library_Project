import functools
import sqlite3

from flask import Flask, url_for
from flask import request, render_template, session, redirect

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def film_dictionary(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class db_connection:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = film_dictionary
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


def get_db_result(query):
    conn = sqlite3.connect('database.db')
    conn.row_factory = film_dictionary
    cur = conn.cursor()
    res = cur.execute(query)
    result = res.fetchall()
    conn.close()
    return result


def decorator_check_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('get_user_login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def main_page():
    result = get_db_result("SELECT * FROM film ORDER by added_info DESC LIMIT 10")
    actors = get_db_result(f"Select * FROM actor JOIN actor_film "
                           f"on actor.id = actor_film.actor_id ")
    genres = get_db_result(f"SELECT * FROM genre_film JOIN film WHERE genre_film.film_id = film.id")
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
    birth_date = request.form["user_birth_date"]
    with db_connection() as cur:
        cur.execute(
            "INSERT INTO user (first_name, last_name, password, login, email, phone_number, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (first_name, last_name, password, login, email, phone_number, birth_date))
    return 'Registered'


@app.route('/login', methods=['GET'])
def get_user_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def complete_user_login():
    login = request.form['login']
    password = request.form['password']
    with db_connection() as cur:
        cur.execute("SELECT * FROM user WHERE login = ? AND password = ?", (login, password))
        result = cur.fetchone()
    if result:
        session['logged_in'] = True
        session['user_id'] = result['id']
        session['first_name'] = result['first_name']
        session['last_name'] = result['last_name']
        return f'Welcome {session["first_name"]} {session["last_name"]}! You are logged in.'
    else:
        return 'Login failed'


@app.route('/logout', methods=['GET'])
@decorator_check_login
def user_logout():
    session.clear()
    return "Logged out"


@app.route('/users/<user_id>', methods=['GET'])
def get_user_id(user_id):
    session_user_id = session.get('user_id')
    with db_connection() as cur:
        cur.execute(f'SELECT * FROM user WHERE id = {user_id}')
        user_by_id = cur.fetchone()
        if session_user_id is None:
            user_by_session = None
        else:
            cur.execute(f'SELECT * FROM user WHERE id = {session_user_id}')
            user_by_session = cur.fetchone()
    return render_template('user_page.html', user=user_by_id, user_session=user_by_session)


@app.route('/users/<user_id>', methods=['POST'])
def update_user_id_profile(user_id):
    session_user_id = session.get('user_id')
    if int(user_id) != session_user_id:
        return 'You can edit only your profile'
    else:
        first_name = request.form["user_first_name"]
        last_name = request.form["user_last_name"]
        password = request.form["password"]
        email = request.form["user_email"]
        phone_number = request.form["user_phone_num"]
        birth_date = request.form["user_birth_date"]
        additional_info = request.form["user_additional_info"]
        with db_connection() as cur:
            cur.execute(
                f"UPDATE user SET first_name='{first_name}', last_name='{last_name}', password='{password}', "
                f"email='{email}', phone_number='{phone_number}', birth_date='{birth_date}', "
                f"additional_info='{additional_info}' WHERE id='{user_id}'")
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
    filter_params = request.args
    filter_list_text = []
    additional_genres_filter = ""
    additional_actors_filter = ""
    for key, value in filter_params.items():
        if value:
            if key == 'name':
                filter_list_text.append(f"name like '%{value}%'")
            elif key == 'genre':
                additional_genres_filter = " JOIN genre_film ON film.id = genre_film.film_id JOIN genre on genre_film.genre_id = genre.genre"
                filter_list_text.append(f"genre.genre like '%{value}%'")
            elif key == 'actor_name':
                additional_actors_filter = " JOIN actor_film ON film.id = actor_film.film_id JOIN actor ON actor_film.actor_id = actor.id "
                filter_list_text.append(
                    f"(actor.actor_first_name LIKE '%{value}%' OR actor.actor_last_name LIKE '%{value}%')")
            else:
                filter_list_text.append(f"{key}='{value}'")
    additional_filter = ""
    if filter_list_text:
        additional_filter = " where " + " and ".join(filter_list_text)
    result = get_db_result(f"SELECT DISTINCT film.* FROM film {additional_genres_filter} {additional_actors_filter} {additional_filter} order by added_info desc")
    actors = get_db_result(f"Select * FROM actor JOIN actor_film "
                           f"on actor.id = actor_film.actor_id ")
    genres = get_db_result(f"SELECT * FROM genre_film JOIN film on genre_film.film_id = film.id")
    genres_selection = get_db_result(
        f"SELECT DISTINCT genre FROM genre JOIN genre_film on genre.genre = genre_film.genre_id")
    countries = get_db_result("SELECT DISTINCT country FROM film order by added_info desc")
    return render_template('films.html', films=result, actors=actors, genres=genres, countries=countries,
                           genres_selection=genres_selection)


@app.route('/films', methods=['POST'])
@decorator_check_login
def add_film():
    return 'Film list updated'


@app.route('/films/<film_id>', methods=['GET'])
def get_film(film_id):
    result = get_db_result(f"SELECT * FROM film WHERE id = {film_id}")
    actors = get_db_result(f"Select * FROM actor JOIN actor_film "
                           f"on actor.id = actor_film.actor_id WHERE actor_film.film_id = {film_id}")
    genres = get_db_result(f"SELECT * FROM genre_film WHERE genre_film.film_id = {film_id}")
    return render_template('film_profile.html', film_list=result, actors=actors, genres=genres)


@app.route('/films/<film_id>', methods=['PUT', 'PATCH'])
@decorator_check_login
def update_film(film_id):
    return f'Film {film_id} updated'


@app.route('/films/<film_id>', methods=['DELETE'])
@decorator_check_login
def delete_film(film_id):
    return f'Film {film_id} deleted'


@app.route('/films/<film_id>/rating', methods=['GET'])
def get_rating(film_id):
    rating = get_db_result(f"SELECT rating FROM film WHERE film.id = {film_id}")
    film_name = get_db_result(f"SELECT name FROM film WHERE film.id ={film_id}")
    return f'Film {film_name} has rating {rating}'


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
    film_name = get_db_result(f"SELECT name FROM film WHERE film.id = {film_id}")
    feedback = get_db_result(
        f"SELECT description FROM feedback WHERE feedback.film_id = {film_id} AND feedback.id = {feedback_id}")
    return f'Film {film_name} has the following feedback: {feedback}'


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
    actor = get_db_result(
        f"SELECT * FROM actor JOIN actor_film on actor.id=actor_film.actor_id WHERE actor.id = {actor_id}")
    films = get_db_result(
        f"SELECT * FROM actor_film JOIN film on actor_film.film_id = film.id WHERE actor_film.actor_id = {actor_id}")
    return render_template("actor_profile.html", actors=actor, films=films)


if __name__ == '__main__':
    app.run()
