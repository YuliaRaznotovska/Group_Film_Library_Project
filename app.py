import sqlite3

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


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


@app.route('/')
def main_page():
    with db_connection() as cur:
        result = cur.execute("SELECT * FROM film ORDER by added_info DESC LIMIT 10").fetchall()
    return result


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
    return 'Logged in'


@app.route('/logout', methods=['GET'])
def user_logout():
    return "Logged out"


@app.route('/users/<user_id>', methods=['GET', 'PATCH'])
def get_user_id(user_id):
    return user_id


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user_id(user_id):
    return 'Deleted'


@app.route('/films', methods=['GET'])
def get_film_list():
    with db_connection() as cur:
        result = cur.execute("SELECT id, poster, name FROM film ORDER by added_info DESC").fetchall()
    return result


@app.route('/films', methods=['POST'])
def add_film():
    return 'Film list updated'


@app.route('/films/<film_id>', methods=['GET'])
def get_film(film_id):
    with db_connection() as cur:
        result = cur.execute(f"SELECT * FROM film WHERE id = {film_id}").fetchall()
        actors = cur.execute(
            f"SELECT * FROM actor JOIN actor_film on actor.id = actor_film.actor_id WHERE actor_film.film_id = {film_id}").fetchall()
        genres = cur.execute(f"SELECT * FROM genre_film WHERE genre_film.film_id = {film_id}").fetchall()
    return f'Film {film_id} is {result}, actors: {actors}, genres: {genres}'


@app.route('/films/<film_id>', methods=['PUT', 'PATCH'])
def update_film(film_id):
    return f'Film {film_id} updated'


@app.route('/films/<film_id>', methods=['DELETE'])
def delete_film(film_id):
    return f'Film {film_id} deleted'


@app.route('/films/<film_id>/rating', methods=['GET'])
def get_rating(film_id):
    with db_connection() as cur:
        rating = cur.execute(f"SELECT rating FROM film WHERE film.id = {film_id}").fetchall()
        film_name = cur.execute(f"SELECT name FROM film WHERE film.id ={film_id}").fetchall()
    return f'Film {film_name} has rating {rating}'


@app.route('/films/<film_id>/rating', methods=['POST'])
def post_rating(film_id):
    return f'Film {film_id} rated'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['GET'])
def get_feedback(film_id, feedback_id):
    return f'Film {film_id} is rated {feedback_id}'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['DELETE'])
def delete_feedback(film_id, feedback_id):
    return f'Film {film_id} feedback {feedback_id} deleted'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['PUT'])
def update_feedback(film_id, feedback_id):
    return f'Film {film_id} feedback is {feedback_id}'


@app.route('/films/<film_id>/rating/<feedback_id>/feedback', methods=['GET'])
def get_feedback_description(film_id, feedback_id):
    with db_connection() as cur:
        film_name = cur.execute(f"SELECT name FROM film WHERE film.id = {film_id}").fetchall()
        feedback = cur.execute(
            f"SELECT description FROM feedback WHERE feedback.film_id = {film_id} AND feedback.id = {feedback_id}").fetchall()
    return f'Film {film_name} has the following feedback: {feedback}'


@app.route('/users/<user_id>/lists', methods=['GET'])
def get_user_lists(user_id):
    return f'{user_id} Lists'


@app.route('/users/<user_id>/lists', methods=['POST'])
def add_list(user_id):
    return f'{user_id} New List'


@app.route('/users/<user_id>/lists/<list_id>', methods=['DELETE'])
def delete_user_list(user_id, list_id):
    return f'{user_id} list {list_id} deleted'


@app.route('/users/<user_id>/lists/<list_id>', methods=['GET'])
def get_watch_later_list(user_id, list_id):
    return f'{user_id} wants to watch {list_id} '


@app.route('/users/<user_id>/lists/<list_id>/<film_id>', methods=['POST'])
def add_film_to_watch_list(user_id, list_id, film_id):
    return f'{user_id} added {film_id} to the list {list_id}'


@app.route('/users/<user_id>/lists/<list_id>/<film_id>', methods=['DELETE'])
def delete_film_from_watch_list(user_id, list_id, film_id):
    return f'{user_id} deleted {film_id} from the list {list_id}'


if __name__ == '__main__':
    app.run()
