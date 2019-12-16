import datetime

import flask
import random
import model
import string
import hashlib
import uuid
import requests

OPENWEATHERMAP_API_KEY = "55d79b326f3720654f6ab31b68231d4a"

from flask import request
from flask import url_for

N_USERS = 10
N_RECEIPES = 10
N_BOOKS = 10

app = flask.Flask(__name__)
db = model.db

db.create_all()


class WeatherInfo:
    def __init__(self,city_name, country, temp, wind_speed, wind_deg):
        self.city_name = city_name
        self.country = country
        self.temp_K = temp
        if self.temp_K is not None:
            self.temp_C = round(self.temp_K - 273, 2)
        else:
            self.temp_C = None
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg

    @staticmethod
    def from_json(json_data):
            city_name = json_data['name']
            country_name = json_data ['sys']['country']
            temp = json_data['main']['temp']
            wind_speed = json_data['wind'].get('speed', 0)
            wind_deg = json_data['wind'].get('deg', 0)
            weather_info = WeatherInfo(
                city_name, country_name, temp, wind_speed, wind_deg
            )
            return weather_info

def get_weather_data(city_name):
    site_url = "api.openweathermap.org/data/2.5/weather"
    city = f"q={city_name}"
    app_id = f"appid={OPENWEATHERMAP_API_KEY}"


    url=f"https://{site_url}?{city}&{app_id}"
    response = requests.get(url)
    json_data = response.json()
    if json_data['cod'] !=200:
        weather_info = WeatherInfo(city_name, None, None, None, None)
    else:
        weather_info = WeatherInfo.from_json(json_data)
    return weather_info


hasher = hashlib.blake2s()


def hash_password(password):
    hasher = hashlib.sha512()
    password = password.encode('utf-8')
    hasher.update(password)
    return hasher.hexdigest()


def create_dummy_users():
    users = []
    for x in range(N_USERS):
        name = "".join(random.choices(string.ascii_lowercase, k=10))
        user = model.User(username=name, email=f"{name}@home.com", password=hash_password(name))
        users.append(user)

    my_user = model.User(username="admin", email="admin@home.com", password=hash_password("admin"))
    users.append(my_user)
    test_user = model.User(username="test", email="test@home.com", password=hash_password("test"))
    users.append(test_user)

    for user in users:
        if not db.query(model.User).filter_by(username=user.username).first():
            db.add(user)
    db.commit()


def create_dummy_receipes():
    receipes = []
    for x in range(N_RECEIPES):
        name = "".join(random.choices(string.ascii_lowercase, k=10))
        name = name.capitalize()
        description = "".join(random.choices(string.ascii_lowercase + "    ", k=80))
        taste = "".join(random.choices(string.ascii_lowercase, k=5))
        new_receipe = model.Receipe(name=name, description=description, taste=taste)
        receipes.append(new_receipe)

    receipe_1 = model.Receipe(name="Apfelstrudel", description="Cut Apple Bake Sweet", taste="sweet")
    receipes.append(receipe_1)
    receipe_2 = model.Receipe(name="Hamburger", description="Fry Meat And Eat", taste="savoury")
    receipes.append(receipe_2)
    receipe_3 = model.Receipe(name="Suppe", description="Cut Carrots Add Water", taste="salty")
    receipes.append(receipe_3)

    for receipe in receipes:
        if not db.query(model.Receipe).filter_by(name=receipe.name).first():
            db.add(receipe)

    db.commit()


def create_dummy_books():
    books = []
    for x in range(N_BOOKS):
        title = "".join(random.choices(string.ascii_lowercase, k=10))
        title = title.capitalize()
        author = "".join(random.choices(string.ascii_lowercase, k=5))
        description = "".join(random.choices(string.ascii_lowercase + "    ", k=80))
        new_book = model.Book(title=title, author=author, description=description)
        books.append(new_book)

        book_1 = model.Book(title="The idiot", author="Fjodor Dostojewski", description="Lorem ipsum")
        books.append(book_1)
        book_2 = model.Book(title="It", author="Stephen King",
                            description="Lorem ipsumsed diam nonumy eirmod tempor invidunt")
        books.append(book_2)
        book_3 = model.Book(title="Wuthering Heights", author="Emily Bronte",
                            description="Lorem ipsum dolor sit amet, conse")
        books.append(book_3)

        for book in books:
            if not db.query(model.Book).filter_by(title=book.title).first():
                db.add(book)

    db.commit()


def add_dummy_data():
    create_dummy_users()
    create_dummy_receipes()
    create_dummy_books()


def require_session_token(func):
    """Decorator to require authentication to access routes"""
    def wrapper(*args, **kwargs):
        session_token = flask.request.cookies.get("session_token")
        redirect_url = flask.request.path or '/'
        if not session_token:
            app.logger.error('no token in request')
            return flask.redirect(flask.url_for('login', redirectTo=redirect_url))
        user = db.query(model.User).filter_by(session_token=session_token).filter(model.User.session_expiry_datetime>=datetime.datetime.now()).first()
        if not user:
            app.logger.error(f'token {session_token} not valid')
            return flask.redirect(flask.url_for('login', redirectTo=redirect_url))
        app.logger.info(f'authenticated user {user.username} with token {user.session_token} valid until {user.session_expiry_datetime.isoformat()}')
        flask.request.user = user
        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper








@app.route("/")
def index():
    return flask.render_template("index.html", myname="Kathi")  # myname platzhalter-variable


@app.route("/fakebook")
def fakebook():
    return flask.render_template("fakebook.html")


@app.route("/portfolio")
def portfolio():
    return flask.render_template("portfolio.html")


@app.route("/about")
def about():
    return flask.render_template("about.html")


@app.route("/secret_number_game")
def secret_number_game():
    return flask.render_template("secret_number_game.html", secret_number=random.randint(1, 10))


@app.route("/blog")
def blog():
    db_receipes = db.query(model.Receipe).filter_by(taste="sweet").all()
    return flask.render_template("blog.html", receipes=db_receipes)


@app.route("/books_add", methods=["GET", "POST"])
def books_add():
    current_request = flask.request

    if current_request.method == "GET":
        return flask.render_template("books_add.html")

    elif current_request.method == "POST":
        # TODO: add valid book
        title = current_request.form.get('title')
        author = current_request.form.get('author')
        description = current_request.form.get('description')
        book_exists = db.query(model.Book).filter_by(title=title, author=author).first()
        if book_exists:
            print("This book already exists")
            return flask.redirect(flask.url_for('books'))
        else:
            new_book = model.Book(title=title, author=author, description=description)
            db.add(new_book)
            db.commit()
            return flask.redirect(flask.url_for('books_add'))


@app.route("/books")
def books():
    all_books = db.query(model.Book).all()
    return flask.render_template("books.html", books=all_books)


@app.route("/books/<book_id>/books_delete", methods=["GET", "POST"])
def books_delete(book_id):
    book_to_delete = db.query(model.Book).get(book_id)
    if book_to_delete is None:
        return flask.redirect(flask.url_for('books'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template("books_delete.html", book=book_to_delete)
    elif current_request.method == "POST":
        db.delete(book_to_delete)
        db.commit()
        return flask.redirect(flask.url_for('books'))
    else:
        return flask.redirect(flask.url_for('books'))


@app.route("/books/<book_id>/edit", methods=["GET", "POST"])
def book_edit(book_id):
    book_to_edit = db.query(model.Book).get(book_id)
    if book_to_edit is None:
        return flask.redirect(flask.url_for('books'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template('books_edit.html', book=book_to_edit)
    elif current_request.method == "POST":
        title = current_request.form.get('title')
        author = current_request.form.get('author')
        description = current_request.form.get('description')

        book_to_edit.title = title
        book_to_edit.author = author
        book_to_edit.description = description

        db.add(book_to_edit)
        db.commit()
        return flask.redirect(flask.url_for('books'))


@app.route("/katzensalon")
def katzensalon():
    return flask.render_template("katzensalon.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    current_request = flask.request

    if current_request.method == "GET":
        return flask.render_template("register.html")

    elif current_request.method == "POST":
        # TODO: register valid user
        email = current_request.form.get('email')
        username = current_request.form.get('username')
        password = current_request.form.get('password')
        user_exists = db.query(model.User).filter_by(username=username).first()
        email_exists = db.query(model.User).filter_by(email=email).first()
        if user_exists:
            print("User already exists")
        elif email_exists:
            print("Email already exists")
        else:
            new_user = model.User(username=username,
                                  email=email,
                                  password=hash_password(password))
            db.add(new_user)
            db.commit()
            return flask.redirect(flask.url_for('register'))


@app.route("/accounts")
@require_session_token
def accounts():

    # get session token
    #current_request = flask.request
    #session_token = current_request.cookies.get('session_token')
    #if not session_token:
        # ToDO: use redirect url to get back to this page after login
       # return flask.redirect(flask.url_for('login', redirectTo='accounts'))
    #user = db.query(model.User).filter_by(session_token=session_token).first()
    #if not user:
        #return flask.redirect(flask.url_for('login', redirectTo='accounts'))
    #if user and not user.session_expiry_datetime>datetime.datetime.now():
        #return flask.redirect(flask.url_for('login', redirectTo='accounts'))

     #user is authenticated, refresh token expiry
    #user.session_expiry_datetime = datetime.datetime.now() + datetime.timedelta(seconds=3600)
   # db. add(user)
    # db.commit()

    all_users = db.query(model.User).all()
    return flask.render_template('accounts.html', accounts=all_users)



@app.route("/accounts/<account_id>/account_delete", methods=["GET", "POST"])
def account_delete(account_id):
    user_to_delete = db.query(model.User).get(account_id)
    if user_to_delete is None:
        return flask.redirect(flask.url_for('accounts'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template("account_delete.html", account=user_to_delete)
    elif current_request.method == "POST":
        db.delete(user_to_delete)
        db.commit()
        return flask.redirect(flask.url_for('accounts'))
    else:
        return flask.redirect(flask.url_for('accounts'))


@app.route("/accounts/<account_id>/edit", methods=["GET", "POST"])
def account_edit(account_id):
    user_to_edit = db.query(model.User).get(account_id)  # get_or_error wirft error aus, wenn Account nicht da ist.
    if user_to_edit is None:
        return flask.redirect(flask.url_for('accounts'))

    current_request = flask.request
    if current_request.method == "GET":
        return flask.render_template('account_edit.html', account=user_to_edit)
    elif current_request.method == "POST":
        email = current_request.form.get('email')
        username = current_request.form.get('username')

        user_to_edit.email = email
        user_to_edit.username = username

        db.add(user_to_edit)
        db.commit()
        return flask.redirect(flask.url_for('accounts'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    current_request = flask.request
    if current_request.method == 'GET':
        return flask.render_template('login.html')
    elif current_request.method == 'POST':
        email = current_request.form.get('email')
        password = current_request.form.get('password')
        user = db.query(model.User).filter_by(email=email).first()
        if user is None:
            print("User does not exist")
            return flask.redirect(flask.url_for('login'))
        else:
            if hash_password(password) == user.password:
                #find redirect method from request argument
                redirect_url = current_request.args.get('redirectTo', '/')

                #generate token end expiry time in 1 hour from now
                session_token = str(uuid.uuid4())
                session_expiry_datetime = datetime.datetime.now() + datetime.timedelta(seconds=3600)
                # update user with new session token and expiry
                user.session_token = session_token
                user.session_expiry_datetime = session_expiry_datetime
                # save in db
                db.add(user)
                db.commit()  #in datenbank drinnen

                # make response and add cookie with session token
                response = flask.make_response(flask.redirect(redirect_url))
                response.set_cookie('session_token', session_token)
                return response
            else:
                return flask.redirect(url_for('forbidden'))



@app.route("/forbidden")
def forbidden():
    return flask.render_template('forbidden.html')

@app.route("/logout")  # token von browser und aus datenbank entfernen
def logout():
    # get session token
    current_request = flask.request
    session_token = current_request.cookies.get('session_token')
    if not session_token:
        # ToDO: use redirect url to get back to this page after login
        return flask.redirect(flask.url_for('login'))
    user = db.query(model.User).filter_by(session_token=session_token).first()
    if not user:
        return flask.redirect(flask.url_for('login'))
    if user and not user.session_expiry_datetime > datetime.datetime.now():
        return flask.redirect(flask.url_for('login'))

    #remove token from db and browser cookie
    user.session_token = None
    user.session_expiry_datetime = None
    db.add(user)
    db.commit()

    return flask.redirect(flask.url_for('login'))

@app.route("/weather/<city_name>", methods=["GET"])
def weather(city_name):
    weather_info = get_weather_data(city_name)
    return flask.render_template('weather.html', weather_info=weather_info)



if __name__ == '__main__':
    add_dummy_data()
    app.run()
