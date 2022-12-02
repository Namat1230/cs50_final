import sqlite3
from helpers import make_standings, convertinput
import sys
import pprint

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/premierleague")
def premierleague():
    input = "Premier League"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), 2022)

    # Close SQL connection
    conn.close()
    return render_template("premierleague.html", standings=standings)

@app.route("/bundesliga")
def bundesliga():
    input = "Bundesliga"
    return render_template("bundesliga.html")

@app.route("/la_liga")
def la_liga():
    input = "La Liga"
    return render_template("la_liga.html")

@app.route("/ligue_one")
def ligue_one():
    input = "Ligue 1"
    return render_template("ligue_one.html")

@app.route("/serie_a")
def serie_a():
    input = "Serie A"
    return render_template("serie_a.html")

# @app.route("/worldcup")
# def worldcup():
#     return render_template("worldcup.html")

@app.route("/betting")
def betting():
    return render_template("betting.html")