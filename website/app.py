from flask import Flask, render_template, request, url_for, redirect
from websiteFunctions import *

# initializes flask, static folder (images and videos and shit) are held in a folder called static
app = Flask(__name__, static_folder='static')

# so in general, app routes are just the directions for what happens at each url.
# for instance, this first one under here just handles the home page, and the next one under it handles website.com/game

# methods post and get represent how the website is feeding information, post is secure, get is public
# whenever the website is loaded originally, it'll use get, whenever a submit button is pressed, it'll use post,
# and then you can follow the different if statements based on those two scenarios

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        global game_type, username, questions, options, favorites_depth, minimum_score
        game_type = request.form["game"]
        username = request.form["username"]
        questions = int(request.form["questions"])
        options = int(request.form["options"])
        favorites_depth = int(request.form["favorites_depth"])
        minimum_score = int(request.form["minimum_show_rating"])
        return redirect(url_for("game"))
    # else being request.method == "GET", so whenever the page is loaded normally do this
    else:
        return render_template("index.html")

# route for the character guessing game page
@app.route("/game", methods=["POST", "GET"])
def game():
    if request.method == "POST":
        return redirect(url_for("results"))
        
    else:
        shows = ["steins gate", "promised neverland", "your moms house"]
        characters = ["mai", "michael", "nick", "gavin", "bene", "tavi", "wes", "william", "hearthy", "jeanette"]
        #character_guess_game(username, questions, options, favorites_depth, minimum_score)
        return render_template("game.html", questions=questions, options=options, shows=shows, characters=characters)

# route for the results page
@app.route("/results")
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run()