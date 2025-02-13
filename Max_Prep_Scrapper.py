from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  

    chrome_driver_path =  

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_table_data(driver):
    url = 'https://www.maxpreps.com/in/greenwood/center-grove-trojans/softball/23-24/stats/#Player'
    driver.get(url)

    time.sleep(10)  
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table', class_='sc-f187837-0 hKBdlI')

    if len(tables) < 2:
        print("Table not found or structure changed.")
        return pd.DataFrame()

    table = tables[1]  
    data = []

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
    driver = setup_driver()
    try:
        df = scrape_table_data(driver)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
    finally:
        driver.quit()

if __name__ == "__main__":
    df = get_player_data()
    print(df)
    df.to_csv("player_stats.csv", index=False)
