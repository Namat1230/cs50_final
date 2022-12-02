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

def make_standings(database):
    # List of league ids we are going to work with, sorted by id
    leagues = database.execute("SELECT id FROM leagues ORDER BY id")
    leagues = [x[0] for x in leagues.fetchall()]

    # Declaring list of list of dictionaries where we are going to store our desired data (easiest way to loop through them in flask afterwards)
    standings = []

    # Loop through the sorted ids and get standings for each league
    for id in leagues:
        tmp = get_standings(id, 2022)
        if not tmp:
            print("Couldn't get standings")
            sys.exit(1)

        # temporary variable to store list of dicionaries of teams
        listofteams = []

        # Store key value pairs that we want to display on our website
        for item in tmp:
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
            listofteams.append(teams)
        # At the end, append each list of teams to standings, creating list of list of dictionaries
        standings.append(listofteams)
    return standings

