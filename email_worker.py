from celery import Celery
from celery.schedules import crontab
from flask import render_template

import database
import email_sender
from app import app as flask_app
from database_queries import get_users, get_new_films

app = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq:5672//')


@app.task
def send_new_film():
    database.init_db()
    with flask_app.app_context():
        new_films = get_new_films()
        email_html = render_template("new_film_email.html", new_films=new_films)
        users = get_users()
        for user in users:
            email_sender.send_email(user.email, email_html)
    return "Emails sent"


app.conf.timezone = 'Europe/Kiev'
app.conf.beat_schedule = {
    'send-new-film-every-minute': {
        'task': 'email_worker.send_new_film',
        'schedule': crontab(hour=2, minute=10),
    },
}
