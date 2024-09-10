import pandas as pd
import json
from modules.constants import CSV_NAME, NAME, NICK, STEAM_ID, ELO, ELO_TG, STARTING_ELO, PLAYERS_JSON_FILE_NAME, MATCHES_JSON_FILE_NAME

# Encode strings as fixed-length byte arrays (not necessary for JSON, but kept for completeness)
def encode_string_list(string_list, length):
    return [s.ljust(length, ' ')[:length] for s in string_list]

# Creates a JSON file with the information on the CSV
def create_jsonfile(json_file_path: str) -> None:
    # Retrieving the data we want to save on the JSON file from the CSV
    csv_df = pd.read_csv(CSV_NAME, index_col=0, dtype={STEAM_ID: str})  # Force SteamID to be read as string
    
    # Convert columns to appropriate types and handle missing values
    csv_df[STEAM_ID] = csv_df[STEAM_ID].fillna('').astype(str)
    csv_df[NAME] = csv_df[NAME].fillna('').astype(str)
    csv_df[NICK] = csv_df[NICK].fillna('').astype(str)
    csv_df[ELO] = csv_df[ELO].fillna(0).astype(int)
    csv_df[ELO_TG] = csv_df[ELO_TG].fillna(0).astype(int)

    aliases = csv_df[NAME].tolist()
    discord_aliases = csv_df[NICK].tolist()
    steam_ids = csv_df[STEAM_ID].tolist()
    elos = csv_df[ELO].tolist()
    elo_tgs = csv_df[ELO_TG].tolist()

    # TODO: Set country, RM elos, and player id from the API call
    elo_internals, elo_internal_tgs, countries, player_ids = [], [], [], []
    for i in range(len(aliases)):
        # Initializing all internal elos to their starting values
        elo_internals.append(STARTING_ELO)
        elo_internal_tgs.append(STARTING_ELO)
        countries.append("Italy")
        player_ids.append(steam_ids[i])

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
            "SteamID": steam_ids[i],  # Keep SteamID as a string
            "PlayerID": player_ids[i]
        }
        players.append(player)

    # Write the data to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(players, json_file, indent=4)


def print_json_contents(json_file_path: str) -> None:
    """
    Reads and prints the contents of a JSON file.

    Parameters:
    json_file_path (str): Path to the JSON file.
    """
    try:
        # Open and read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Print the JSON data
        print(json.dumps(data, indent=4))
    
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    
    except json.JSONDecodeError:
        print("Error: The file could not be decoded. Ensure it is a valid JSON file.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import json

def print_steam_ids(json_file_path: str) -> None:
    """
    Reads a JSON file, extracts SteamID values, converts them to long integers,
    and prints them.

    Parameters:
    json_file_path (str): Path to the JSON file.
    """
    try:
        # Open and read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Extract and convert SteamID values
        steam_ids = []
        for player in data:
            steam_id_str = player.get('SteamID', '0')  # Default to '0' if 'SteamID' is missing
            try:
                steam_id_int = int(steam_id_str) 
                steam_ids.append(steam_id_int)
            except ValueError:
                # setting steam_id to -1 when an error occurs (probably missing steam_id, blank field in json) 
                steam_ids.append(-1)
        
        # Print SteamID values
        print("SteamIDs (as long integers):")
        for steam_id in steam_ids:
            print(steam_id)
    
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    
    except json.JSONDecodeError:
        print("Error: The file could not be decoded. Ensure it is a valid JSON file.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import json

def retrieve_data_from_json(json_file_path: str):
    """
    Reads data from a JSON file and stores it in separate lists for each attribute.

    Parameters:
    json_file_path (str): Path to the JSON file.

    Returns:
    dict: A dictionary containing lists of data for each attribute.
    """
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Initialize lists
        aliases = []
        discord_aliases = []
        steam_ids = []
        elos = []
        elo_tgs = []
        elo_internals = []
        elo_internal_tgs = []
        countries = []
        player_ids = []

        # Populate lists from JSON data
        for player in data:
            aliases.append(player.get('Alias', ''))
            discord_aliases.append(player.get('Discord Alias', ''))
            steam_ids.append(player.get('SteamID', ''))
            elos.append(player.get('Elo', 0))
            elo_tgs.append(player.get('EloTG', 0))
            elo_internals.append(player.get('EloInternal', 0))
            elo_internal_tgs.append(player.get('EloInternalTG', 0))
            countries.append(player.get('Country', ''))
            player_ids.append(player.get('PlayerID', ''))

        # Return a dictionary containing all lists
        return {
            'aliases': aliases,
            'discord_aliases': discord_aliases,
            'steam_ids': steam_ids,
            'elos': elos,
            'elo_tgs': elo_tgs,
            'elo_internals': elo_internals,
            'elo_internal_tgs': elo_internal_tgs,
            'countries': countries,
            'player_ids': player_ids
        }

    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: The file could not be decoded. Ensure it is a valid JSON file.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


if __name__ == "__main__":
    
    create_jsonfile(PLAYERS_JSON_FILE_NAME)
    #retrieves players data from the json file
    data = retrieve_data_from_json(PLAYERS_JSON_FILE_NAME)
    print(data)





