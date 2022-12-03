import sqlite3
from helpers import make_standings, convertinput, get_last_round, get_next_round
import sys
import pprint

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from collections import OrderedDict

import os

from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required


# Define constant for the season year
season = 2022

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///soccerbase.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Routes
@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        # Gets username, passsword, and confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        elif not password:
            return apology("must provide password", 400)

        elif not confirmation:
            return apology("must provide confirmation", 400)

        elif password != confirmation:
            return apology("password and confirmation do not match", 400)

        # Hashes password
        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already taken", 400)

        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/premierleague")
@login_required
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
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("premierleague.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/bundesliga")
@login_required
def bundesliga():
    input = "Bundesliga"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("bundesliga.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/la_liga")
@login_required
def la_liga():
    input = "La Liga"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("la_liga.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/ligue_one")
@login_required
def ligue_one():
    input = "Ligue 1"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("ligue_one.html", standings=standings, thead = thead, last = last, next = next)

@app.route("/serie_a")
@login_required
def serie_a():
    input = "Serie A"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)


    # Close SQL connection
    conn.close()

    return render_template("serie_a.html", standings=standings, thead = thead, last = last, next = next)

# @app.route("/worldcup")
# def worldcup():
#     return render_template("worldcup.html")

@app.route("/betting")
@login_required
def betting():
    return render_template("betting.html")