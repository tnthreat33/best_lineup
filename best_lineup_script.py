import pandas as pd
import subprocess
import os

def run_scraper():
    print("Fetching latest player stats...")
    subprocess.run(["python", "Max_Prep_Scrapper.py"], check=True)
    print("Scraping complete.\n")

def load_player_data():
    if not os.path.exists("player_stats.csv"):
        print("No existing player stats found. Running scraper...")
        run_scraper()

    try:
        df = pd.read_csv("player_stats.csv")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print("Error: player_stats.csv not found. Ensure the scraper runs correctly.")
        return []

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

def display_lineup(lineup):
    print("\nOptimized Lineup:")
    for i, player in enumerate(lineup, start=1):
        if player:
            print(f"{i}. {player['Player']} (OBP: {player['OBP']}, SLG: {player['SLG']}, SB: {player['SB']})")
        else:
            print(f"{i}. (Empty Slot)")

if __name__ == "__main__":
    run_scraper() 
    players = load_player_data()
    lineup = generate_best_lineup(players)
    display_lineup(lineup)
