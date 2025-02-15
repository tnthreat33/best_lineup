import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table_data():
    url = 'https://www.maxpreps.com/in/greenwood/center-grove-trojans/softball/23-24/stats/#Player'
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table (adjust the class name as needed)
    tables = soup.find_all('table', class_='sc-f187837-0 hKBdlI')

    if len(tables) < 2:
        print("Table not found or structure changed.")
        return pd.DataFrame()

    table = tables[1]  # Adjust the index if needed
    data = []

    # Extract data from the table
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        
        name = columns[1].find('a').text.strip()
        obp = float(columns[11].text.strip()) if columns[11].text.strip() != '-' else 0.0
        slg = float(columns[12].text.strip()) if columns[12].text.strip() != '-' else 0.0
        sb = int(columns[13].text.strip()) if columns[13].text.strip().isdigit() else 0  

        data.append({
            'Player': name,
            'OBP': obp,
            'SLG': slg,
            'SB': sb
        })

    return pd.DataFrame(data)

def get_player_data():
    try:
        df = scrape_table_data()
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = get_player_data()
    print(df)
    df.to_csv("player_stats.csv", index=False)