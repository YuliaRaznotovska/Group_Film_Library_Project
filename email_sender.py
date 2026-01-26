import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, html_content):
    user = os.environ.get("EMAIL_USER")
    pwd = os.environ.get("EMAIL_PASSWORD")
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Meet new films"
    msg['From'] = FROM
    msg['To'] = ", ".join(TO)

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.send_message(msg)
        print(f"Successfully sent the mail to {TO}")
    except Exception as e:
        print(f"Failed to send mail to {TO}: {e}")
