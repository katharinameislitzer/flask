import flask
import random
import model

from flask import url_for

app = flask.Flask(__name__)
# db = model.db
# db.create_all()


@app.route("/")
def index():
   # user = model.User(id=1, username="Wolfi", email="wolfi@haus.at")
  #  db.add(user)
    # db.commit()

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
    receipe_1 = model.Receipe("Apfelstrudel", "Cut Apple Bake Sweet", "sweet")
    receipe_2 = model.Receipe("Hamburger", "Fry Meat And Eat", "savioury")
    receipe_3 = model.Receipe("Suppe", "Cut Carrots Add Water", "salty")

    return flask.render_template("blog.html", receipes=[receipe_1, receipe_2, receipe_3])


@app.route("/books")
def books():
    book_1 = model.Book("The idiot", "Dostojewski", "Lorem ipsum")
    book_2 = model.Book("It", "King", "Lorem ipsumsed diam nonumy eirmod tempor invidunt")
    book_3 = model.Book("Wuthering Heights", "Bronte", "Lorem ipsum dolor sit amet, conse")

    return flask.render_template("books.html", books=[book_1, book_2, book_3])

@app.route("/katzensalon")
def katzensalon():
    return flask.render_template("katzensalon.html")

if __name__ == '__main__':
    app.run()
