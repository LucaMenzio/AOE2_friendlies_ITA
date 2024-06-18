from modules.elo import Elo
from modules.game.player import Player

player1 = Player(
    profile_id="aaaaaa",
    steam_id="bbbbbb",
    elo_1v1=Elo(1000),
    elo_tg=Elo(1000),
    elo_ingame=Elo(1000),
    elo_tg_ingame=Elo(1000),
)


player2 = Player(
    profile_id="ccccccc",
    steam_id="dddddd",
    elo_1v1=Elo(2000),
    elo_tg=Elo(2000),
    elo_ingame=Elo(2000),
    elo_tg_ingame=Elo(2000),
)


def test():
    print("Hello World")
