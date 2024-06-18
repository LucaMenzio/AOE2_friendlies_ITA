from modules.elo import Elo
from modules.game.player import Player


class Team:
    def __init__(
        self, p1: Player, p2: Player, p3: Player | None = None, p4: Player | None = None
    ) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

        self._validate_player_numbers()
        self._size = self._compute_size()

    def _compute_size(self) -> int:
        size = 2
        return size + bool(self.p3) + bool(self.p4)

    def _validate_player_numbers(self) -> None:
        if self.p4 and not self.p3:
            raise ValueError("Can't assign a player #4 without giving player #3")

    def _compute_team_elo(self) -> Elo:
        return Elo.team_elo([player.elo_tg for player in self.players])

    @property
    def elo(self) -> Elo:
        value = int(sum([player.elo_tg.elo for player in self.players]) / self.size)
        return Elo(value)

    @property
    def size(self) -> int:
        return self._size

    # TODO: maybe replace with an iterator
    @property
    def players(self) -> list["Player"]:
        players = [self.p1, self.p2]
        if self.p3:
            players.append(self.p3)
        if self.p4:
            players.append(self.p4)
        return players

    @property
    def elos(self) -> list[int]:
        elos = []
        for player in self.players:
            elos.append(player.elo_tg)
        return elos

    def from_list(self, players: list[Player]) -> "Team":
        """
        Class Constructor based on a list of Players
        """
        return Team(*players)
