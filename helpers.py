import requests
import json
import sqlite3
import pprint
from collections import OrderedDict

# These are the leagues we will be working with; they are the top 5 most watched leagues
our_leagues = {
    "Premier League" : "England",
    "Bundesliga" : "Germany",
    "La Liga" : "Spain",
    "Serie A" : "Italy",
    "Ligue 1" : "France"
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
        print("Couldn't connect to API")
        return False

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
    return True

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
    return response["response"][0]["league"]["standings"][0]

def make_standings(league_id, season_year):

    # Temporary variable where we store API's output
    tmp = get_standings(league_id, season_year)
    if not tmp:
        print("Couldn't get standings")
        sys.exit(1)

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
        teams["Goalsfor"] = item["all"]["goals"]["for"]
        teams["Goalsagainst"] = item["all"]["goals"]["against"]

        # Append the temp dictionary to our list
        listofteams.append(teams)

    # Return list of teams (dictionaries)
    return listofteams

# Convert league name input to an id
def convertinput(database, league_name):
    id = database.execute("SELECT id FROM leagues WHERE name = ?", [league_name])
    id = id.fetchone()
    id = id[0]
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
    response = response["response"][0]["league"]["round"]
    return response

# Get the fixtures that are in the next/last round
def get_fixture(league_id, season_year, next_or_last):
    # Getting the name of next round
    round = get_round(league_id, season_year, next_or_last)
    if not round:
        print("Couldn't get round")
        sys.exit(1)

    # API documentation for getitng a response for fixtures in the next/last round
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season_year}&round={round}"

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
        print("Couldn't get next round")
        sys.exit(1)
    fixtures = []
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
        print("Couldn't get last round")
        sys.exit(1)
    fixtures = []
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