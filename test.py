import requests

from modules.api.getRecentMatchHistory import getRecentMatchHistory
from modules.api.sql_orm import MatchhistorystatTable
from modules.constants import MY_STEAM_ID

resp_matches = requests.get(
    "https://aoe-api.worldsedgelink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22%2Fsteam%2F"
    + str(MY_STEAM_ID)
    + "%22]"
).json()

api_response = getRecentMatchHistory(**resp_matches)
# match = MatchhistorystatTable(**api_response.matchHistoryStats[0].model_dump())

match_raw = api_response.matchHistoryStats[0].model_dump()

MatchhistorystatTable(**match_raw)


MATCH_JSON = {
    "match_id": 1,
    "match_players": [
        {"profile_id": 1, "civilization_id": 1},
        {"profile_id": 2, "civilization_id": 2},
    ],
    "match_items": [
        {"item_id": 1},
        {"item_id": 2},
    ],
}


# class Item(SQLModel):
#     item_id: int
#     match_id: int = Field(foreign_key="mymatch.match_id", default=None)
#     match: "MyMatch" = Relationship(back_populates="match_players")


# class Players(SQLModel):
#     profile_id: int
#     civilization_id: int
#     match_id: int = Field(foreign_key="mymatch.match_id", default=None)
#     match: "MyMatch" = Relationship(back_populates="match_players")


# class MyMatch(SQLModel):
#     match_id: int
#     match_players: list[Players] = Relationship(back_populates="match")
#     match_items: list[Item] = Relationship(back_populates="match")


# my_match = MyMatch(**MATCH_JSON)
# # player_1 = MATCH_JSON["match_players"][0]

# players = [
#     Players(
#         **player,
#         match=my_match,
#     )
#     for player in MATCH_JSON["match_players"]
# ]

# items = [
#     Item(
#         **item,
#         match=my_match,
#     )
#     for item in MATCH_JSON["match_items"]
# ]

# print(f"{my_match=}")
# print(f"{players=}")
# print(f"{items=}")
