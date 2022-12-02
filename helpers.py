import requests
import json
import sqlite3
import pprint

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

    # returning response in a json format
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

    # returning the response we want in a json format
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
        teams = {}
        teams.update({"rank" : item["rank"]})
        teams.update({"name" : item["team"]["name"]})
        teams.update({"logo" : item["team"]["logo"]})
        teams.update({"points" : item["points"]})
        teams.update({"played" : item["all"]["played"]})
        teams.update({"win" : item["all"]["win"]})
        teams.update({"draw" : item["all"]["draw"]})
        teams.update({"lose" : item["all"]["lose"]})
        teams.update({"goalsfor" : item["all"]["goals"]["for"]})
        teams.update({"goalsagainst" : item["all"]["goals"]["against"]})

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
def get_next_or_last_round(league_id, season_year, next_or_last):
    # API documentation for getitng a response for standings
    url = f"https://v3.football.api-sports.io/fixtures?season={season_year}&league={league_id}&{next_or_last}=1"

    payload={}
    headers = {
        'x-rapidapi-key': 'c4b2f02de36f4916cc87ab129e628422',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # returning the response we want in a json format
    response = requests.request("GET", url, headers=headers, data=payload).json()
    response = response["response"][0]["league"]["round"]
    return response

