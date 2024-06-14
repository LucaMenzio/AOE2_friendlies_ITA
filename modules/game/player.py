from modules.elo import Elo


class Player:
    def __init__(
        self,
        profile_id: str,
        steam_id: str,
        elo_1v1: Elo,
        elo_tg: Elo,
        elo_ingame: Elo,
        elo_tg_ingame: Elo,
    ) -> None:
        self.profile_id = profile_id
        self.steam_id: str = steam_id
        self._elo: Elo = elo_1v1
        self._elo_tg: Elo = elo_tg
        self._elo_ingame: Elo = elo_ingame
        self._elo_tg: Elo = elo_tg_ingame

    @property
    def elo(self) -> Elo:
        return self._elo

    @property
    def elo_tg(self) -> Elo:
        return self._elo_tg

    def update_win(self, other: "Player") -> None:
        """
        Update Elo of self after winning against other

        Args:
            other (Player): loser player
        """
        raise NotImplementedError

    def update_loss(self, other: "Player") -> None:
        """
        Update Elo of self after losing against other

        Args:
            other (Player): winner player
        """
        raise NotImplementedError

    # TODO: write interface for other in case of team
    def update_win_tg(self, other) -> None:
        """
        Update Elo of self after winning against other Team

        Args:
            other (???): loser team
        """
        raise NotImplementedError

    # TODO: write interface for other in case of team
    def update_loss_tg(self, other):
        """
        Update Elo of self after losing against other Team


        Args:
            other (???): winner team
        """
        raise NotImplementedError


class PlayerAPI:
    def __init__(
        self,
        profile_id,
        name,
        alias,
        personal_statgroup_id,
        xp,
        level,
        leaderboardregion_id,
        country,
    ):
        self.profile_id: str = profile_id
        self.name: str = name
        self.alias: str = alias
        self.personal_statgroup_id: str = personal_statgroup_id  # TODO: what is this?
        self.xp: int = xp
        self.level: int = level  # TODO: what is this?
        self.leaderboardregion_id: str = leaderboardregion_id
        self.country: str = country
        self.steam_id: str = self._get_steam_id(name)

    def _get_steam_id(self, name: str) -> str:
        """
        From the available API, "name" is f"/steam/{STEAM_ID}"

        Returns:
            str: given "name" from the API, it returns STEAM_ID
        """
        return name.split("/")[-1]
