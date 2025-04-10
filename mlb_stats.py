import statsapi
import requests
from datetime import date

GIANTS_TEAM_ID = 137
START_DATE = "2025-03-27"
END_DATE = date.today().isoformat() 

url = (
    f"https://statsapi.mlb.com/api/v1/schedule"
    f"?sportId=1&teamId={GIANTS_TEAM_ID}&startDate={START_DATE}&endDate={END_DATE}"
)

response = requests.get(url)
data = response.json()

# Print game date, opponent, and score if available
for date_info in data.get("dates", []):
    for game in date_info.get("games", []):
        game_date = game["gameDate"][:10]
        home_team = game["teams"]["home"]["team"]["name"]
        away_team = game["teams"]["away"]["team"]["name"]
        status = game["status"]["detailedState"]
        print(f"{game_date} - {away_team} @ {home_team} - Status: {status}")

        if status == "Final":
            home_score = game["teams"]["home"]["score"]
            away_score = game["teams"]["away"]["score"]
            print(f"    Final Score: {away_team} {away_score} - {home_team} {home_score}")