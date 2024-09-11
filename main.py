from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask import Flask, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_KEY")
Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    # Email setup
    sender_email = os.getenv("EMAIL")   # Replace with your email address
    receiver_email = os.getenv("MY_EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")  # Replace with your email password

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'New Contact Form Submission'

    body = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # server.starttls()
            server.login(user=sender_email, password=email_password)
            server.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=msg.as_string())
        return redirect(url_for('success'))
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('error'))


@app.route('/success')
def success():
    return "Form submission successful! Thank you."


@app.route('/error')
def error():
    return "Error sending message. Please try again later."


if __name__ == "__main__":
    app.run(debug=False, port=5003)
