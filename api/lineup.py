from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
from api.Max_Prep_Scrapper import get_player_data

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        df = get_player_data()
        print("Fetched DataFrame:", df)
        if df.empty:
            print("No data returned from get_player_data()")
        players = df.to_dict(orient="records")
        lineup = generate_best_lineup(players)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(lineup).encode())

def generate_best_lineup(players):
    if not players:
        print("No player data available.")
        return []
    players_sorted = sorted(players, key=lambda x: x["OBP"], reverse=True)
    # Assign top 3 players to 1st, 4th, and 2nd spots
    core_three = [players_sorted[0], players_sorted[1], players_sorted[2]]
    core_three_sorted = sorted(core_three, key=lambda x: x["SLG"], reverse=True)
    lineup = [None] * 9
    lineup[3] = core_three_sorted[0]  
    remaining_core = [core_three_sorted[1], core_three_sorted[2]]
    remaining_core_sorted = sorted(remaining_core, key=lambda x: x["OBP"], reverse=True)
    lineup[0] = remaining_core_sorted[0]  
    lineup[1] = remaining_core_sorted[1]  

    # Assign 4th and 5th highest OBP to spots 5 and 6
    lineup[2] = players_sorted[3]
    lineup[4] = players_sorted[4]

    # Assign remaining players based on OBP, prioritizing stolen bases for spot 6
    remaining_players = players_sorted[5:9]
    remaining_players_sb = sorted(remaining_players, key=lambda x: x["SB"], reverse=True)
    remaining_obp_player = [remaining_players_sb[1], remaining_players_sb[2], remaining_players_sb[3]]
    last_obp_sort = sorted(remaining_obp_player, key=lambda x: x["OBP"], reverse=True)
    lineup[5] = remaining_players_sb[0]
    lineup[6:] = last_obp_sort[:3]  
    return lineup
