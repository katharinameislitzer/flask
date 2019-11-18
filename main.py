import flask
import random
import model
app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html", myname="Kathi") #myname platzhalter-variable

@app.route("/fakebook")
def fakebook():
    return flask.render_template("fakebook.html")

@app.route("/portfolio")
def portfolio():
    return flask.render_template("portfolio.html")

@app.route("/about")
def about():
    return flask.render_template("about.html")

@app.route("/secret-number-game")
def secret_number_game():
    return flask.render_template("secret_number_game.html", secret_number=random.randint(1,10))

@app.route("/blog")
def blog():

    receipe_1 = model.Receipe("Apfelstrudel", "Cut Apple Bake Sweet", "sweet")
    receipe_2 = model.Receipe("Hamburger", "Fry Meat And Eat", "savioury")
    receipe_3 = model.Receipe("Suppe", "Cut Carrots Add Water", "salty")

    return flask.render_template("blog.html", receipes=[receipe_1, receipe_2, receipe_3])




if __name__ == '__main__':
    app.run()
