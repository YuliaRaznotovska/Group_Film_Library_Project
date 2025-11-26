import sqlite3

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    res = cur.execute("SELECT id, poster, name FROM film ORDER by added_info DESC LIMIT 10")
    result = res.fetchall()
    return result


@app.route('/register', methods=['GET'])
def get_user_registration():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def complete_user_registration():
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
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    res = cur.execute("SELECT id, poster, name FROM film ORDER by added_info DESC")
    result = res.fetchall()
    return result


@app.route('/films', methods=['POST'])
def add_film():
    return 'Film list updated'


@app.route('/films/<film_id>', methods=['GET'])
def get_film(film_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM film WHERE id = ?", (film_id,))
    result = res.fetchone()
    actors = cur.execute(
        "SELECT * FROM actor JOIN actor_film on actor.id = actor_film.actor_id WHERE actor_film.film_id = ?",
        (film_id,)).fetchall()
    genres = cur.execute("SELECT * FROM genre_film WHERE genre_film.film_id = ?", (film_id,)).fetchall()
    return f'Film {film_id} is {result}, actors: {actors}, genres: {genres}'


@app.route('/films/<film_id>', methods=['PUT', 'PATCH'])
def update_film(film_id):
    return f'Film {film_id} updated'


@app.route('/films/<film_id>', methods=['DELETE'])
def delete_film(film_id):
    return f'Film {film_id} deleted'


@app.route('/films/<film_id>/rating', methods=['GET'])
def get_rating(film_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    rating = cur.execute("SELECT rating FROM film WHERE film.id = ?", (film_id,)).fetchone()
    film_name = cur.execute("SELECT name FROM film WHERE film.id =?", (film_id,)).fetchone()
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
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    film_name = cur.execute("SELECT name FROM film WHERE film.id =?", (film_id,)).fetchone()
    feedback = cur.execute("SELECT description FROM feedback WHERE feedback.film_id = ? AND feedback.id = ?",
                           (film_id, feedback_id)).fetchone()
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
