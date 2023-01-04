from flask import Flask, render_template, request, url_for, redirect
from websiteFunctions import *

app = Flask(__name__, static_folder='static')

# starting page will just be index.html, the shit with all the forms
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        game = request.form["game"]
        username = request.form["username"]
        questions = request.form["questions"]
        options = request.form["options"]
        favorites_depth = request.form["favorites_depth"]
        minimum_score = request.form["minimum_show_rating"]

        global user_inputs
        user_inputs = [game, username, questions, options, favorites_depth, minimum_score]
        return redirect(url_for("user", usr=username))
    else:
        return render_template("index.html")
    
@app.route("/<usr>")
def user(usr):
    game = user_inputs[0]
    username = user_inputs[1]
    questions = int(user_inputs[2])
    options = int(user_inputs[3])
    favorites_depth = int(user_inputs[4])
    minimum_score = int(user_inputs[5])
    character_guess_game(username, questions, options, favorites_depth, minimum_score)
    return f"<h1>{user_inputs}</h1>"

if __name__ == "__main__":
    app.run()