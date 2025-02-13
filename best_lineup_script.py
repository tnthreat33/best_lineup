import pandas as pd

players = [
    {"Player": "M. Munson", "OBP": 0.453, "SLG": 0.414, "SB": 21},
    {"Player": "K. Hardin", "OBP": 0.296, "SLG": 0.348, "SB": 4},
    {"Player": "A. Krupa", "OBP": 0.356, "SLG": 0.512, "SB": 2},
    {"Player": "M. Tharpe", "OBP": 0.471, "SLG": 0.525, "SB": 2},
    {"Player": "R. Janda", "OBP": 0.549, "SLG": 1.124, "SB": 22},
    {"Player": "E. Burris", "OBP": 0.4, "SLG": 0.308, "SB": 5},
    {"Player": "B. Meyer", "OBP": 0.5, "SLG": 0.602, "SB": 21},
    {"Player": "B. Groppel", "OBP": 0.277, "SLG": 0.432, "SB": 2},
    {"Player": "H. Haberstroh", "OBP": 0.598, "SLG": 0.75, "SB": 22},
    {"Player": "A. Powel", "OBP": 0.472, "SLG": 0.621, "SB": 1},
    {"Player": "s. Hermann", "OBP": 0.448, "SLG": 0.739, "SB": 3},
    {"Player": "E.Baird", "OBP": 0.4, "SLG": 0.308, "SB": 0},
    {"Player": "A.Rchards", "OBP": 0.364, "SLG": 0.4, "SB": 0},
    {"Player": "t.Barrett", "OBP": 0.258, "SLG": 0.402, "SB": 3},
    {"Player": "A.Wolff", "OBP": 0.222, "SLG": 0.22, "SB": 3}
]

# Sort players by OBP descending
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

def display_lineup(lineup):
    print("Optimized Lineup:")
    for i, player in enumerate(lineup, start=1):
        if player:
            print(f"{i}. {player['Player']} (OBP: {player['OBP']}, SLG: {player['SLG']}, SB: {player['SB']})")
        else:
            print(f"{i}. (Empty Slot)")

display_lineup(lineup)