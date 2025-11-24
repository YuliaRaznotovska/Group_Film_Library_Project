from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def main_page():  # put application's code here
    return 'Hello World!'


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
    return 'Film list'


@app.route('/films', methods=['POST'])
def add_film():
    return 'Film list updated'


@app.route('/films/<film_id>', methods=['GET'])
def get_film(film_id):
    return f'Film {film_id}'


@app.route('/films/<film_id>', methods=['PUT', 'PATCH'])
def update_film(film_id):
    return f'Film {film_id} updated'


@app.route('/films/<film_id>', methods=['DELETE'])
def delete_film(film_id):
    return f'Film {film_id} deleted'


@app.route('/films/<film_id>/rating', methods=['GET'])
def get_rating(film_id):
    return f'Film {film_id} rating'


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
