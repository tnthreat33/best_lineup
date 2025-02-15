from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
from api.Max_Prep_Scrapper import get_player_data

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        df = get_player_data()
        players = df.to_dict(orient="records")
        lineup = generate_best_lineup(players)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(lineup).encode())

def generate_best_lineup(players):
    if not players:
        return []
    players_sorted = sorted(players, key=lambda x: x["OBP"], reverse=True)
    lineup = [None] * 9
    lineup[3] = players_sorted[0]  
    lineup[0] = players_sorted[1]  
    lineup[1] = players_sorted[2]  
    lineup[2] = players_sorted[3]
    lineup[4] = players_sorted[4]
    lineup[5:] = players_sorted[5:9]
    return lineup
