import sqlite3
from helpers import make_standings, convertinput, get_last_round, get_next_round, apology, login_required, get_fixture_ids, get_odds, get_fixtures_info
import sys
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import pprint

# Define constant for the season year
season = 2022

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies) – Finance
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# From finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Routes
@app.route("/")
@login_required # Do we need login required for the home page?
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
        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = rows.fetchall()

        # Ensure username exists and password is correct
        if not len(rows) or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        # Close SQL connection
        conn.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

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

        # Check if username is taken
        check = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        check = check.fetchone()
        if check:
            conn.close
            return apology("username is taken", 400)

        # Insert user into database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                       (username, generate_password_hash(request.form.get("password"))))
            conn.commit()

        # Log In user
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = user.fetchone()
        session["user_id"] = user
        # Close SQL connection
        conn.close()

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

@app.route("/worldcup")
def worldcup():

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Gets the id of fixtures we are going to display
    fixtures = get_fixture_ids(convertinput(db, input), season)

    # Returns dictionary of odds, in format of home away for every fixture
    odds = get_odds(convertinput(db, input), season, fixtures)

    # Gets the information about fixtures
    info = get_fixtures_info(fixtures)



    return render_template("worldcup.html")

@app.route("/betting")
@login_required
def betting():
    return render_template("betting.html")