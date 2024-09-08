import uproot
import numpy as np
import pandas as pd 
from modules.constants import CSV_NAME, NAME, NICK, STEAM_ID, ELO, ELO_TG, STARTING_ELO, ROOTFILE_NAME, PLAYERS_TREE, GAMES_TREE

# Retrieving the data we want to save on the rootfile from the csv
csv_df = pd.read_csv(CSV_NAME, index_col=0, dtype={"Steam ID": "str"})

aliases = csv_df[NAME]
discord_aliases = csv_df[NICK]
steam_ids = csv_df[STEAM_ID]
elos = csv_df[ELO]
elo_tgs = csv_df[ELO_TG]

print(discord_aliases,steam_ids,elos,elo_tgs)

'''
elo_internals, elo_internal_tgs = [], []
for i in range(len(aliases)):
    # Initializing all internal elos to their starting values
    elo_internals.append(STARTING_ELO)
    elo_internal_tgs.append(STARTING_ELO)



# Populate the players list in a loop
players = []
for i in range(len(aliases)):
    player = {
        "Alias": aliases[i],
        "Discord Alias": discord_aliases[i],
        "EloInternal": elo_internals[i],
        "EloInternalTG": elo_internal_tgs[i],
        "Elo": elos[i],
        "EloTG": elo_tgs[i],
        "Country": countries[i],
        "SteamID": steam_ids[i],
        "PlayerID": player_ids[i]
    }
    players.append(player)

# Create a new ROOT file
root_file = uproot.recreate(ROOTFILE_NAME)

# Defines the structure of the branches with the corresponding data types
branches = {
    "Alias": "string",             # Main Nickname
    "EloInternal": "int32",        # 1v1 Elo, Internal rankings
    "EloInternalTG": "int32",      # TG Elo, Internal rankings
    "Elo": "int32",                # 1v1 Elo
    "EloTG": "int32",              # TG Elo
    "Country": "string",           # Country of origin
    "SteamID": "int64[]",          # SteamID(s)
    "PlayerID": "int64[]"          # PlayerID(s)
}

# Create the tree with the name from constants.PLAYERS_TREE
tree = root_file[PLAYERS_TREE] = uproot.newtree(branches)

for player in players:
    tree["Alias"].extend([player["Alias"]])
    tree["EloInternal"].extend([player["EloInternal"]])
    tree["EloInternalTG"].extend([player["EloInternalTG"]])
    tree["Elo"].extend([player["Elo"]])
    tree["EloTG"].extend([player["EloTG"]])
    tree["Country"].extend([player["Country"]])
    tree["SteamID"].extend([player["SteamID"]])
    tree["PlayerID"].extend([player["PlayerID"]])



# Close the ROOT file to save the changes
root_file.close()
'''