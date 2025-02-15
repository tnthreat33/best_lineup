import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Access the API key from environment variables
SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY')

def scrape_table_data():
    url = "https://www.maxpreps.com/in/greenwood/center-grove-trojans/softball/23-24/stats/#Player"

    # ScraperAPI request to fetch the rendered HTML content
    payload = {
        "api_key": SCRAPER_API_KEY,  # Use the environment variable here
        "url": url,
        "render": "true"  # Ensures JavaScript is executed
    }

    # Make the request to ScraperAPI
    response = requests.get("https://api.scraperapi.com/", params=payload, timeout=30)  


    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame()

    # Parse the fetched HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table containing the stats (ensure this class is correct)
    tables = soup.find_all("table", class_="sc-f187837-0 hKBdlI")

    if len(tables) < 2:
        print("Table not found or structure changed.")
        return pd.DataFrame()

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

    # Return the extracted data as a pandas DataFrame
    return pd.DataFrame(data)

def get_player_data():
    try:
        df = scrape_table_data()
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Get player data and print it
    df = get_player_data()
    print(df)
    df.to_csv("player_stats.csv", index=False)
