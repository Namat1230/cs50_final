from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session



# Configure application
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/premierleague")
def premierleague():
    return render_template("premierleague.html")

@app.route("/bundesliga")
def bundesliga():
    return render_template("bundesliga.html")

@app.route("/la_liga")
def la_liga():
    return render_template("la_liga.html")

@app.route("/ligue_one")
def ligue_one():
    return render_template("ligue_one.html")

@app.route("/serie_a")
def serie_a():
    return render_template("serie_a.html")

@app.route("/worldcup")
def worldcup():
    return render_template("worldcup.html")

@app.route("/betting")
def betting():
    return render_template("betting.html")