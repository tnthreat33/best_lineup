import pandas as pd
import json
from api.Max_Prep_Scrapper import get_player_data  # Import the refactored scraper

def generate_best_lineup(players):
    if not players:
        print("No player data available.")
        return []

    players_sorted = sorted(players, key=lambda x: x["OBP"], reverse=True)
    lineup = [None] * 9
    lineup[3] = players_sorted[0]  # Best OBP and SLG
    lineup[0] = players_sorted[1]  # Second-best OBP
    lineup[1] = players_sorted[2]  # Third-best OBP
    lineup[2] = players_sorted[3]
    lineup[4] = players_sorted[4]
    lineup[5:] = players_sorted[5:9]
    return lineup

def handler(event, context):
    # Fetch player data using the refactored scraper
    df = get_player_data()
    players = df.to_dict(orient="records")

    # Generate the lineup
    lineup = generate_best_lineup(players)

    # Return the lineup as a JSON response
    return {
        "statusCode": 200,
        "body": json.dumps(lineup)
    }