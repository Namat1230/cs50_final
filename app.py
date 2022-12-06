import sqlite3
from helpers import make_standings, convertinput, get_last_round, get_next_round, apology, login_required, get_fixture_ids, get_odds, get_fixtures_info, check_bet, get_status
import sys
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


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
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

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
            return apology("invalid username or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

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

        # Check inputs
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must provide confirmation", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # Hashes password
        hash = generate_password_hash(password)

        # Check if username is taken
        check = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        check = check.fetchall()
        if len(check):
            conn.close
            return apology("username is taken", 400)

        # Insert user into database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", (username, hash))
            conn.commit()

        # Log In user
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = user.fetchone()
        session["user_id"] = user[0]

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

    # Make standings according to user input and gather all information we need to display in our page
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)

    # Close SQL connection
    conn.close()
    return render_template("premierleague.html", standings=standings, thead=thead, last=last, next=next)

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

    # Make standings according to user input and gather all information we need to display in our page
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)

    # Close SQL connection
    conn.close()

    return render_template("bundesliga.html", standings=standings, thead=thead, last=last, next=next)

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

    # Make standings according to user input and gather all information we need to display in our page
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)

    # Close SQL connection
    conn.close()

    return render_template("la_liga.html", standings=standings, thead=thead, last=last, next=next)

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

    # Make standings according to user input and gather all information we need to display in our page
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)

    # Close SQL connection
    conn.close()

    return render_template("ligue_one.html", standings=standings, thead=thead, last=last, next=next)

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

    # Make standings according to user input and gather all information we need to display in our page
    standings = make_standings(convertinput(db, input), season)
    thead = standings[0]
    last = get_last_round(convertinput(db, input), season)
    next = get_next_round(convertinput(db, input), season)

    # Close SQL connection
    conn.close()

    return render_template("serie_a.html", standings=standings, thead=thead, last=last, next=next)

@app.route("/wcbetting", methods=["GET", "POST"])
@login_required
def worldcup():
    input = "World Cup"

    if request.method == "GET":

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

        if not odds or not fixtures or not info:
            return apology("No bets available", 400)

        length = len(info)
        conn.close()
        return render_template("wcbetting.html", odds = odds, info = info, length = length, fixtures = fixtures)

    else:
        # Get info form forms
        fixture = request.form.get("fixture")
        team = request.form.get("team")
        odds = request.form.get("odds")
        money = request.form.get("money")

        # Check inputs
        if not fixture or not team or not odds:
            return apology("Click a Button to Bet", 400)
        if not money:
            return apology("Put in Money", 400)
        if not money.isdigit():
            return apology("Invalid amount", 400)

        # Min bet 10$
        money = int(money)
        if money < 10:
            return apology("The minimum bet amount is 10$")

        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Update user balance
        current = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
        current = current.fetchone()
        current = int(current[0])
        money = int(money)
        if current < money:
            return apology("Cannot afford")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", (current-money, session["user_id"]))
            conn.commit()

        # Update bets history
        db.execute("INSERT INTO bets (user_id, amount, fixture, bet, odds) VALUES (?, ?, ?, ?, ?)",
                  ((session["user_id"]), money, fixture, team, odds))
        conn.commit()
        conn.close()
        return redirect("/account")

@app.route("/wcstandings")
@login_required
def wcstandings():
    input = "World Cup"

    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Make standings according to user input and gather all information we need to display in our page
    standings = make_standings(convertinput(db, input), season)
    index = list(standings.keys())
    index = index[0]
    thead = standings[index][0]
    # Close SQL connection
    conn.close()
    return render_template("wcstandings.html", standings = standings, thead = thead)

@app.route("/account")
@login_required
def account():
    # Connect to our database
    try:
        conn = sqlite3.connect("soccerbase.db")
        db = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        sys.exit(1)

    # Store the information for all bets of the user
    bets = db.execute("SELECT * FROM bets WHERE user_id = ?", (session["user_id"],))
    bets = bets.fetchall()

    # Lists that we will display in html page
    display = []
    results = []
    details = []

    # Loop through every bet
    for item in bets:

        # Info that we will display, appennd to the list we will use
        info = get_fixtures_info(item[2])
        display.append(info)

        # Details of the bet
        tmp = []
        tmp.append(item[3])
        tmp.append(item[1])
        tmp.append(item[6])
        tmp.append(item[5])

        # Check the status of the bet and change it accordingly; Bet is stil active

        if check_bet(item[2]):
            status = "Active"
        else:
            # Bet won, update user cash according to the odds and his bet amount
            result = get_status(item[2])
            if result[item[3]]["winner"]:
                status = "Bet Won"

                # We need to check if we already paid the user, if not, we want to pay him for his win
                payment = db.execute("SELECT * FROM transactions WHERE user_id = ? AND fixture = ?", (session["user_id"], item[2]))
                payment = payment.fetchall()
                if not payment:
                    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (int(item[1]*item[6]), session["user_id"]))
                    conn.commit()
                    db.execute("INSERT INTO transactions (user_id, fixture) VALUES (?, ?)", (session["user_id"], item[2]))
                    conn.commit()
            else:
                # Bet lost
                status = "Bet Lost"

        # Update lists for every bet
        results.append(status)
        details.append(tmp)

    # Check user balance, we will display it on the website
    balance = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
    balance = balance.fetchone()
    balance = balance[0]
    length = len(results)
    conn.close()
    return render_template("account.html", balance=balance, display=display, results=results, length=length, details=details)

@app.route("/changepassword", methods=["GET", "POST"])
def password():
    """Change password"""

    # For method post
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old"):
            return apology("provide old password", 403)

        # Ensure new password was submitted
        elif not request.form.get("new"):
            return apology("provide new password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Ensure old password is correct
        old = request.form.get("old")
        oldhash = db.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],))
        oldhash = oldhash.fetchone()
        oldhash = oldhash[0]
        if not check_password_hash(oldhash, old):
            return apology("old password incorrect", 403)

        # Ensure passwords match
        confirmation = request.form.get("confirmation")
        if request.form.get("new") != confirmation:
            return apology("passwords do not match", 400)

        # Ensure old and new passwords are not the same
        if confirmation == old:
            return apology("select a new password", 400)

        # Create new password and logout the user
        db.execute("UPDATE users SET hash = ? WHERE id = ?", (generate_password_hash(confirmation), session["user_id"]))
        conn.commit()
        conn.close()
        return redirect("/logout")

    # For method get
    else:
        return render_template("changepassword.html")


@app.route("/additionalcash", methods=["GET", "POST"])
@login_required
def additionalcash():
    """Adding Additional Cash"""

    if request.method == "GET":
        return render_template("additionalcash.html")
    else:
        add_cash = request.form.get("add_cash")

        # Check input
        if not add_cash:
            return apology("Add Money", 400)

        if not add_cash.isdigit():
            return apology("Invalid amount", 400)

        add_cash = int(add_cash)

        # Connect to our database
        try:
            conn = sqlite3.connect("soccerbase.db")
            db = conn.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            sys.exit(1)

        # Update cash
        user_id = session["user_id"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (add_cash, user_id))
        conn.commit()
        conn.close()
        return redirect("/account")