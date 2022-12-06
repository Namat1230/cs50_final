from functools import wraps
import requests
from collections import OrderedDict
from flask import redirect, render_template, session

# Portion of code from finance
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# Code from finance to require login for certain pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# These are the leagues we will be working with; they are the top 5 most watched leagues + World cup
our_leagues = {
    "Premier League" : "England",
    "Bundesliga" : "Germany",
    "La Liga" : "Spain",
    "Serie A" : "Italy",
    "Ligue 1" : "France",
    "World Cup" : "World"
}

# No need to run this function in app.py! We already called this function and gathered the data we needed and pasted it in SQL database
# To call this function, import get_leagues_stats and our_leagues from helpers into app py and paste appropriate arguments
# Only need to call this function when we change our desired leagues
def get_leagues_stats(leagues, connection, database):

    # API documentation for getitng a response for active leagues
    url = "https://v3.football.api-sports.io/leagues?current=true"

    payload = {}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning response in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()

    if not response:
        return apology("API error", 400)

    # Delete existing data
    database.execute("DELETE FROM leagues")
    connection.commit()

    # Insert information in a SQL database
    response = response["response"]
    for dictionary in response:
        if dictionary["league"]["name"] in leagues.keys() and dictionary["country"]["name"] == leagues[dictionary["league"]["name"]]:
            database.execute("INSERT INTO leagues (id, name, logo, country, country_flag, start, end) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (dictionary["league"]["id"], dictionary["league"]["name"], dictionary["league"]["logo"], dictionary["country"]["name"],
                         dictionary["country"]["flag"], dictionary["seasons"][0]["start"], dictionary["seasons"][0]["end"]))
            connection.commit()
    return

def get_standings(league_id, season_year):

    # API documentation for getitng a response for standings
    url = f"https://v3.football.api-sports.io/standings?league={league_id}&season={season_year}"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    try:
        response = response["response"][0]["league"]["standings"]
    except:
        return apology("Couldn't get standings", 403)

    # Return the first element if the lenght is 1, else return the whole list
    if len(response) > 1:
        return response
    else:
        return response[0]

def make_standings(league_id, season_year):

    # Temporary variable where we store API's output
    tmp = get_standings(league_id, season_year)

    # Check if the list is a list of lists (we have groups in standings)
    if any(isinstance(el, list) for el in tmp):

        # Return dictionary
        groups = {}

        # Loop through every group
        for group in tmp:

            # Variable to store list of dicionaries (teams) that is going to be returned
            listofteams = []

            # Store key value pairs that we want to display on our website
            for item in group:

                # Temporary dictionary
                teams = OrderedDict()
                teams["Rank"] = item["rank"]
                teams["Name"] = item["team"]["name"]
                teams["Logo"] = item["team"]["logo"]
                teams["Points"] = item["points"]
                teams["Played"] = item["all"]["played"]
                teams["Win"] = item["all"]["win"]
                teams["Draw"] = item["all"]["draw"]
                teams["Lose"] = item["all"]["lose"]
                teams["Goals For"] = item["all"]["goals"]["for"]
                teams["Goals Against"] = item["all"]["goals"]["against"]

                # Append the temp dictionary to our list
                listofteams.append(teams)
            groups[group[0]["group"]] = listofteams

        # Return list of teams (dictionaries)
        return groups
    else:

        # Variable to store list of dicionaries (teams) that is going to be returned
        listofteams = []

        # Store key value pairs that we want to display on our website
        for item in tmp:
            # Temporary dictionary
            teams = OrderedDict()
            teams["Rank"] = item["rank"]
            teams["Name"] = item["team"]["name"]
            teams["Logo"] = item["team"]["logo"]
            teams["Points"] = item["points"]
            teams["Played"] = item["all"]["played"]
            teams["Win"] = item["all"]["win"]
            teams["Draw"] = item["all"]["draw"]
            teams["Lose"] = item["all"]["lose"]
            teams["Goals For"] = item["all"]["goals"]["for"]
            teams["Goals Against"] = item["all"]["goals"]["against"]

            # Append the temp dictionary to our list
            listofteams.append(teams)

        # Return list of teams (dictionaries)
        return listofteams

# Convert league name input to an id, this way we can make it dynamic according to the route
def convertinput(database, league_name):

    id = database.execute("SELECT id FROM leagues WHERE name = ?", [league_name])
    id = id.fetchone()
    try:
        id = id[0]
    except:
        return apology("No information available", 400)
    return id

# Get the name of either last or next round of a league depending on the input, we will use this to display it on the website and access data
def get_round(league_id, season_year, next_or_last):
    # API documentation for getitng a response for name of next/last round
    url = f"https://v3.football.api-sports.io/fixtures?season={season_year}&league={league_id}&{next_or_last}=1"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    try:
        response = response["response"][0]["league"]["round"]
    except:
        return apology("Could not get next round", 400)
    return response

# Get the fixtures that are in the next/last round
def get_fixture(league_id, season_year, next_or_last):
    # Getting the name of next round
    round = get_round(league_id, season_year, next_or_last)

    # Status will help us display only the matches we want
    if next_or_last == "next":
        status = "NS-TBD"
    else:
        status = "FT-AET-PEN"

    # API documentation for getitng a response for fixtures in the next/last round
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season_year}&round={round}&status={status}"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return response["response"]

# Preparing our return value for usage in flask for next round
def get_next_round(league_id, season_year):
    response = get_fixture(league_id, season_year, "next")

    if not response:
        return apology("No matches available", 400)

    # Return list
    fixtures = []

    # Loop trhough all matches and store the info we want in a dictionary
    for item in response:

        # Temporary dictionary
        tmp = OrderedDict()
        tmp["hlogo"] = item["teams"]["home"]["logo"]
        tmp["Home"] = item["teams"]["home"]["name"]
        tmp["Away"] = item["teams"]["away"]["name"]
        tmp["alogo"] = item["teams"]["away"]["logo"]

        # Append the tmp dictionary to our list
        fixtures.append(tmp)
    return fixtures

# Preparing our return value for usage in flask for previous round
def get_last_round(league_id, season_year):
    response = get_fixture(league_id, season_year, "last")

    if not response:
        return apology("No matches available", 400)

    # Here we store our return values
    fixtures = []

    # Loop trhough all matches and store the info we want in a dictionary
    for item in response:
        # Temporary dictionary
        tmp = OrderedDict()
        tmp["hlogo"] = item["teams"]["home"]["logo"]
        tmp["Home"] = item["teams"]["home"]["name"]
        tmp["hgoals"] = item["goals"]["home"]
        tmp["agoals"] = item["goals"]["away"]
        tmp["Away"] = item["teams"]["away"]["name"]
        tmp["alogo"] = item["teams"]["away"]["logo"]

        # Append the tmp dictionary to our list
        fixtures.append(tmp)
    return fixtures

def get_fixture_ids(league_id, season_year):
    response = get_fixture(league_id, season_year, "next")

    if not response:
        return apology("No matches available", 400)

    # List of fixture ids
    fixtures = []
    for item in response:

        # Append ids to the list
        fixtures.append(item["fixture"]["id"])
    return fixtures

def get_odds(league_id, season_year, fixtures):

    # Return list
    odds = []

    # Ids that will be deleted from fixtures
    delete = []
    for id in fixtures:

        # API documentation for getitng a response for fixtures in the next/last round
        url = f"https://v3.football.api-sports.io/odds?league={league_id}&season={season_year}&bet=2&fixture={id}&bookmaker=6"

        payload={}
        headers = {
            'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        # Returning the response we want in a json format
        response = requests.request("GET", url, headers=headers, data=payload).json()
        response = response["response"]

        # If we get a response
        if not response:
            delete.append(id)
        else:

            # Temporary dictionary
            tmp = OrderedDict()
            try:
                tmp["home"] = response[0]["bookmakers"][0]["bets"][0]["values"][0]["odd"]
            except:
                tmp["home"] = "No Odds"
            try:
                tmp["away"] = response[0]["bookmakers"][0]["bets"][0]["values"][1]["odd"]
            except:
                tmp["away"] = "No Odds"
            odds.append(tmp)
    for item in delete:
        fixtures.remove(item)
    return odds

# Get the info about fixtures we will display
def get_fixtures_info(fixtures):
    if isinstance(fixtures, list):
        string = '-'.join(str(id) for id in fixtures)
    else:
        string = fixtures

    # API documentation for getitng a response for fixtures in the next/last round
    url = f"https://v3.football.api-sports.io/fixtures?ids={string}"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    response = response["response"]

    if not response:
        return apology("No matches available", 400)

    # Return list
    info = []
    for dictionary in response:
        # Temporary dictionary
        tmp = OrderedDict()
        tmp["hlogo"] = dictionary["teams"]["home"]["logo"]
        tmp["home"] = dictionary["teams"]["home"]["name"]
        tmp["away"] = dictionary["teams"]["away"]["name"]
        tmp["alogo"] = dictionary["teams"]["away"]["logo"]
        info.append(tmp)
    return info

def check_bet(fixture):

    # API documentation for getitng a response for fixtures in the next/last round
    url = f"https://v3.football.api-sports.io/fixtures?id={fixture}"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    try:
        response = response["response"][0]
    except:
        return apology("Could not check bet", 400)

    if response["teams"]["home"]["winner"] == None:
        return True
    else:
        return False

def get_status(fixtures):

    # If our input is multiple fixtures, we turn them into a string
    if isinstance(fixtures, list):
        string = '-'.join(str(id) for id in fixtures)
    else:
        string = fixtures

    # API documentation for getitng a response for fixtures in the next/last round
    url = f"https://v3.football.api-sports.io/fixtures?ids={string}"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    try:
        response = response["response"][0]["teams"]
    except:
        return apology("Could not get status", 400)
    return response

# Check if number is float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False