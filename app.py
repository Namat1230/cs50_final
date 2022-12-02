import sqlite3
from helpers import make_standings
import sys
import pprint

# Connect to our database
try:
    conn = sqlite3.connect("soccerbase.db")
    db = conn.cursor()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
    sys.exit(1)

standings = make_standings(db)
pprint.pprint(standings)

# Close SQL connection
conn.close()