import sqla_wrapper
import os

# SQLITE_FILE = ':memory:'
SQLITE_FILE = 'localhost.sqlite'



db = sqla_wrapper.SQLAlchemy(os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_FILE}"))
db = sqla_wrapper.SQLAlchemy("postgres://ihrjaqphsudkfb:548a06250244aacae612ff7be72a57fae7ce0983d829850d6c259b1cc911afc3@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/d47t7li5vvl594")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  #  Nullable definiert, ob Pflichtfeld oder nicht
    session_token = db.Column(db.String, nullable=True)
    session_expiry_datetime = db.Column(db.DateTime, nullable=True)


class Receipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String, unique=True)
    taste = db.Column(db.String, unique=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    author = db.Column(db.String, unique=True)
    description = db.Column(db.String, unique=True)
