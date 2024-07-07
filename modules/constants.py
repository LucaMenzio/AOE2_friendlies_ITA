import os
from enum import Enum

from dotenv import load_dotenv

ELO_K = 30.0

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
