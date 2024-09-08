import os
from enum import Enum

from dotenv import load_dotenv

# Constant K for elo calculation 
ELO_K = 30.0

# Average (and starting) Elo. Set to 1400, approximately the average elo of the italian server players 
STARTING_ELO = 1400

load_dotenv()
MY_STEAM_ID = os.getenv("MY_STEAM_ID")


class MatchType(Enum):
    NULL = 0
    RM_1v1 = 6
    RM_TG = 7
    QP_2v2 = 19
    QP_3v3 = 20
    QP_4v4 = 21


# Columns name in .csv files
NAME = "Names"
NICK = "Discord Nick"
STEAM_ID = "Steam ID"
ELO = "Elo 1v1"
ELO_TG = "Elo tg"

# Main csv name
CSV_NAME = "files/elo_aoe2italia_internal.csv"

# Name of the rootfile
ROOTFILE_NAME = "DB_Aoe2Italia.root"

# Names of the trees inside the rootfile
PLAYERS_TREE = "Players"
GAMES_TREE = "Games"