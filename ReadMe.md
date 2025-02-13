# Softball Lineup Optimizer

This project scrapes softball player stats from MaxPreps and generates the best lineup based on On-Base Percentage (OBP), Slugging Percentage (SLG), and Stolen Bases (SB).

## 🚀 Features
- **Web Scraping**: Uses Selenium & BeautifulSoup to extract player stats.
- **Automated Lineup Optimization**: Sorts and positions players for maximum efficiency.
- **Seamless Integration**: The lineup script automatically runs the scraper before generating results.

## 📂 Project Structure
📦 baseball-lineup-optimizer 
┣ 📜 best_lineup_script.py # Runs scraper & generates the best lineup 
┣ 📜 Max_Prep_Scraper.py # Scrapes latest player stats & saves to CSV 
┣ 📜 player_stats.csv # Cached player data (generated automatically) 
┣ 📜 README.md # Project documentation


## 🛠 Requirements
- Python 3.x
- `selenium`
- `beautifulsoup4`
- `pandas`
- `chromedriver` (Ensure the path is correctly set in `Max_Prep_Scraper.py`)

## 🔧 Setup & Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/baseball-lineup-optimizer.git
   cd baseball-lineup-optimizer
2. Set up ChromeDrive and update path in Max_Prep_Scapper.py
3. run python best_lineup_script.py
