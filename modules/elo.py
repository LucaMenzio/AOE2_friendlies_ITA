from typing import Self, Sequence

from modules.utils import exactly_one_kw_only_arg


class Elo:
    """
    Represent a generic Elo
    It implements elo win/loss changes
    """

    def __init__(self, elo: int) -> None:
        self._elo: int = elo

    @property
    def elo(self):
        """Elo value"""
        return self._elo

    def update_elo(self, change: int):
        self._elo += change

    @staticmethod
    def compute_elo_change(winner: "Elo", loser: "Elo") -> int:
        """
        Compute elo points won

        Args:
            winner (Elo): Elo of winner
            loser (Elo): Elo of loser

        Returns:
            int: changes in Elo for winner
        """
        raise NotImplementedError

    @exactly_one_kw_only_arg
    def update_win(
        self, *, other: Self | None = None, others: Sequence[Self] | None = None
    ) -> None:
        """
        Update Elo after winning against other(s)

        Args:
            other (Self | None, optional):
                Elo of the loser player. If None, `others` should be given
            others (Sequence[Self] | None, optional):
                Elos of each member of the loser team. If None, `other` should be given
        """
        if other is None:
            assert others is not None
        if others is None:
            assert other is not None
            others = [other]

        others_elo = self.team_elo(others)
        change = self.compute_elo_change(self, others_elo)
        self.update_elo(change)

    @exactly_one_kw_only_arg
    def update_loss(
        self, *, other: Self | None = None, others: Sequence[Self] | None = None
    ) -> None:
        """
        Update Elo after losing against other(s)

        Args:
            other (Self | None, optional):
                Elo of the winner player. If None, `others` should be given
            others (Sequence[Self] | None, optional):
                Elos of each member of the winner team. If None, `other` should be given
        """
        if other is None:
            assert others is not None
        if others is None:
            assert other is not None
            others = [other]

        others_elo = self.team_elo(others)
        change = self.compute_elo_change(others_elo, self)
        self.update_elo(change)

    @staticmethod
    def team_elo(players: Sequence["Elo"]) -> "Elo":
        """
        Compute the combined Elo of players

        Args:
            players (Sequence[Elo]): list of players Elos

        Returns:
            Elo: Elo object with the combined elo
        """
        elo = int(sum([player.elo for player in players]) / len(players))
        return Elo(elo)
