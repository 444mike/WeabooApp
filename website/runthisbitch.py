from flask import Flask, redirect, url_for, render_template
import sys
#sys.path.insert('C:\Users\444mi\OneDrive\Desktop\WeebProject\website\functions.py')
#from functions import write_df

app = Flask(__name__)

@app.route("/")
def home():
    with open("dataframe.txt", "r") as f:
        res = f.readlines()
    return render_template("index.html", content=["penis", "dick"])



if __name__ == "__main__":
    app.run()

