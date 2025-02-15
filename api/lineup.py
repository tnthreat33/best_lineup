from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from bs4 import BeautifulSoup

# Access the API key from environment variables
SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY')

# Function to fetch and process player data
def scrape_table_data():
    url = "https://www.maxpreps.com/in/greenwood/center-grove-trojans/softball/23-24/stats/#Player"

    # ScraperAPI request to fetch the rendered HTML content
    payload = {
        "api_key": SCRAPER_API_KEY,  # Use the environment variable here
        "url": url,
        "render": "true"  # Ensures JavaScript is executed
    }

    # Make the request to ScraperAPI
    response = requests.get("https://api.scraperapi.com/", params=payload, timeout=10)  

    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

    # Parse the fetched HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table containing the stats (ensure this class is correct)
    tables = soup.find_all("table", class_="sc-f187837-0 hKBdlI")

    if len(tables) < 2:
        print("Table not found or structure changed.")
        return []

    table = tables[1]  # Adjust if needed
    data = []

    # Extract data from each row of the table
    for row in table.find("tbody").find_all("tr"):
        columns = row.find_all("td")

        # Extract player name, OBP, SLG, SB
        name = columns[1].find("a").text.strip()
        obp = float(columns[11].text.strip()) if columns[11].text.strip() != "-" else 0.0
        slg = float(columns[12].text.strip()) if columns[12].text.strip() != "-" else 0.0
        sb = int(columns[13].text.strip()) if columns[13].text.strip().isdigit() else 0  

        # Add the player's data to the list
        data.append({"Player": name, "OBP": obp, "SLG": slg, "SB": sb})

    # Return the extracted data
    return data

# Function to generate the best lineup
def generate_best_lineup(players):
    if not players:
        print("No player data available.")
        return []
    players_sorted = sorted(players, key=lambda x: x["OBP"], reverse=True)
    core_three = [players_sorted[0], players_sorted[1], players_sorted[2]]
    core_three_sorted = sorted(core_three, key=lambda x: x["SLG"], reverse=True)
    lineup = [None] * 9
    lineup[3] = core_three_sorted[0]  
    remaining_core = [core_three_sorted[1], core_three_sorted[2]]
    remaining_core_sorted = sorted(remaining_core, key=lambda x: x["OBP"], reverse=True)
    lineup[0] = remaining_core_sorted[0]  
    lineup[1] = remaining_core_sorted[1]  

    lineup[2] = players_sorted[3]
    lineup[4] = players_sorted[4]

    remaining_players = players_sorted[5:9]
    remaining_players_sb = sorted(remaining_players, key=lambda x: x["SB"], reverse=True)
    remaining_obp_player = [remaining_players_sb[1], remaining_players_sb[2], remaining_players_sb[3]]
    last_obp_sort = sorted(remaining_obp_player, key=lambda x: x["OBP"], reverse=True)
    lineup[5] = remaining_players_sb[0]
    lineup[6:] = last_obp_sort[:3]  
    return lineup

# Handler class for the HTTP request
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Fetch player data
        players = scrape_table_data()
        if not players:
            print("No data fetched.")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Failed to fetch player data"}).encode())
            return
        
        # Generate the best lineup
        lineup = generate_best_lineup(players)

        # Send the response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(lineup).encode())

