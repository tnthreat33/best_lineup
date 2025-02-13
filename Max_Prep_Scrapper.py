from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  

    chrome_driver_path =  # Replace with your actual path

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Scrape the table data
def scrape_table_data(driver):
    url = 'https://www.maxpreps.com/in/greenwood/center-grove-trojans/softball/23-24/stats/#Player'
    driver.get(url)

    time.sleep(10) 
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table', class_='sc-f187837-0 hKBdlI')

    if not tables:
        print("No tables found. Check if the class name or structure has changed.")
        return []

    if len(tables) < 2:
        print("Only one table found. The second table is missing.")
        return []

    table = tables[1]

    data = []

    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        
        name = columns[1].find('a').text.strip()
        
        obp = columns[11].text.strip()  
        slg = columns[12].text.strip()  
        
        data.append({
            'Name': name,
            'OBP': obp,
            'SLG': slg
        })

    return data

def main():
    driver = setup_driver()

    try:
        data = scrape_table_data(driver)

        for entry in data:
            print(entry)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()