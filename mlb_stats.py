import statsapi
import requests
import psycopg2
import os
from datetime import date
from dotenv import load_dotenv

#TODO: uncomment after rest works
"""
# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("supabase_user")
PASSWORD = os.getenv("supabase_password")
HOST = os.getenv("supabase_host")
PORT = os.getenv("supabase_port")
DBNAME = os.getenv("supabase_dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
"""

GIANTS_TEAM_ID = 137
START_DATE = "2025-03-27"
END_DATE = "2025-04-10"

url = (
    f"https://statsapi.mlb.com/api/v1/schedule"
    f"?sportId=1&teamId={GIANTS_TEAM_ID}&startDate={START_DATE}&endDate={END_DATE}"
)

response = requests.get(url)
data = response.json()

#id (autogen), date (YYYY-MM-DD), opponent, win (bool), runs_for (int), runs_against (int), home (bool)

for date_info in data.get("dates", []):
    for game in date_info.get("games", []):
        date = game["gameDate"][:10]
        home_team = game["teams"]["home"]["team"]["name"]
        away_team = game["teams"]["away"]["team"]["name"]
        
        if home_team == "San Francisco Giants":
            opponent = away_team
            home = True
        else:
            opponent = home_team
            home = False

        if home:
            runs_for = game["teams"]["home"]["score"]
            runs_against = game["teams"]["away"]["score"]
        else:
            runs_for = game["teams"]["away"]["score"]
            runs_against = game["teams"]["home"]["score"]

        win = True if runs_for > runs_against else False

        print(f"INSERT INTO games (date, opponent, win, runs_for, runs_against, home) VALUES ('{date}', '{opponent}', {win}, {runs_for}, {runs_against}, {home});")