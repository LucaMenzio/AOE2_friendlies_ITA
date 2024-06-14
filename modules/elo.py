class Elo:
    """
    Represent a generic Elo.
    It implements elo win/loss changes
    """

    def __init__(self, elo: int) -> None:
        self._elo: int = elo

    @property
    def elo(self):
        """
        Elo value
        """
        return self._elo

    @staticmethod
    def compute_elo(elo1: "Elo", elo2: "Elo") -> int:
        """
        Compute elo changes given a player with elo1 winning
        against a player with elo2

        Args:
            elo1 (Elo): Winner
            elo2 (Elo): Loser
        """
        raise NotImplementedError

    def update_win(self, other: "Elo") -> None:
        """
        Update Elo if wins against other

        Args:
            other (Elo): the loser elo
        """
        raise NotImplementedError

    def update_loss(self, other: "Elo") -> None:
        """
        Update Elo if loses against other

        Args:
            other (Elo): the winner elo
        """
        raise NotImplementedError
