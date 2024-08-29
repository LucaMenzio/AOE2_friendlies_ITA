import numpy as np
import csv
import pandas as pd

from itertools import combinations
from typing import Union
from modules.constants import NAME, NICK, ID, ELO, ELO_TG

# constant for elo calculation
K = 30.0


class AOE2ItaliaElo:
    """Main class to read, write and update the csv file containing ELOs of all players"""
    def __init__(self, file_name: str):
        self.fileName = file_name
        self.fileName_timestamps = "files/game_timestamps.csv"
        
        # getting all the info from the csv
        self.df = pd.read_csv(self.fileName, index_col=0)
        self.df[[ID, ELO, ELO_TG]] = self.df[[ID, ELO, ELO_TG]].astype("Int64")
        self.df_timestamps = pd.read_csv(self.fileName_timestamps, index_col=0)

    # returns the 1v1 elo for a given player name
    def get_elo1v1(self, player_name: str):
        return self._get_record_given_value(player_name, NAME, ELO)

    # TODO: it works only if the searched values (id, nick, name) are unique. Verify that
    def _get_record_given_value(
        self, value: str, column: str, get: str
    ) -> Union[str, int]:
        """
        Basically, a VLOOKUP of 'value' in 'column', and it returns the values from the column 'get'.
        Return -1 if 'value' is not found

        Args:
            value (str): a name, steam_id, or discord name
            column (str): column to use to search for 'value'
            get (str): value to return

        Returns:
            _type_: _description_
        """
        if value not in self.df[column].values:
            return -1

        df_temp = self.df.set_index(column)
        return df_temp.loc[value][get]

    # returns the 1v1 elo for a given player steam id
    def get_elo1v1_by_id(self, player_steam_id: int):
        return self._get_record_given_value(player_steam_id, ID, ELO)

    # returns the tg elo for a given player name
    def get_elotg(self, player_name: str):
        return self._get_record_given_value(player_name, NAME, ELO_TG)

    # returns the tg elo for a given player name
    def get_elotg_by_id(self, player_steam_id: int):
        return self._get_record_given_value(player_steam_id, ID, ELO_TG)

    #TODO: not sure what it should return exactly. Compare with previous code. If the same name is written twice, it will fail. 
    # returns two teams balanced with respect of the sigle's tg elos
    def balance_teams_internal(self, team_names) -> list:
        difference = 1000

        # checks to avoid shenanigans
        if len(team_names) % 2 != 0:
            print("Number of players is odd, check it and try again")
            return -1
        if len(team_names) == 2:
            print("No need for balancing here")
            return team_names
        for name in team_names:
            if (self.df[NAME] == name).sum() == 0:
                print(f"{name} not found!")
                return -1
        # finished with checks

        df = self.df.query(f"{NAME} in {team_names}")
        total_elo = df[ELO_TG].sum()

        for team_a, team_b in list(combinations(df["Names"], len(df) / 2)):
            team_a_elo = df[df[NAME].isin(team_a)][ELO_TG].sum()
            if difference > abs(team_a_elo - total_elo / 2):
                good_a, good_b = team_a, team_b
                difference = abs(team_a_elo - total_elo / 2)
        return [good_a, good_b]

    # balances the teams by providing the elos only
    def balance_teams(self, elos: list):
        difference = 1000
        team = [-1, -1, -1]
        if len(elos) % 2 != 0:
            print("Number of players is odd, check it and try again")
            return -1
        if len(elos) == 2:
            print("No need for balancing")
            return -2

        team.clear()
        n = len(elos)
        print(elos)
        sum_elo = sum(elos)
        possible_combinations = list(combinations(elos, int(n / 2)))
        for team_a, team_b in possible_combinations:
            team_a_elo = sum(team_a)
            if difference > abs(team_a_elo - sum_elo / 2):
                good_a, good_b = team_a, team_b
                difference = abs(team_a_elo - sum_elo / 2)
        return [good_a, good_b]

    # sets the elo
    def set_elo(self, player_name: str, new_elo: int):
        if player_name not in self.df[NAME].values:
            return -1
        self.df.loc[self.df[NAME] == player_name, ELO] = new_elo

    # gets the player nickname given a certain steam id
    def get_name(self, player_steam_id: int):
        return self._get_record_given_value(player_steam_id, ID, NICK)

    # gets the steam id corresponding to a certain player name
    def get_steam_id(self, player_name: str):
        return self._get_record_given_value(player_name, NAME, ID)

    # computes the new elo of p1, assuming constant K
    def compute_elo(self, elo_p1: int, elo_p2: int, won):
        p1 = 1.0 / (1.0 + np.power(10, (elo_p2 - elo_p1) / 400))
        return elo_p1 + K * (won - p1)

    def update_elo(self, steam_id: int, new_elo: int, is_1v1: bool):
        if steam_id not in self.df[ID].values:
            return -1
        if is_1v1:
            self.df.loc[self.df[ID] == steam_id, ELO] = new_elo
        else:
            self.df.loc[self.df[ID] == steam_id, ELO_TG] = new_elo

    # TODO: why is "steam_id" a string?
    # allows to add a player to the database
    def add_player(self, name: str, steam_id, elo_1v1: int, elo_tg: int):
        if (
            isinstance(name, str)
            and isinstance(steam_id, str)
            and isinstance(elo_1v1, int)
            and isinstance(elo_tg, int)
        ):
            new_player = {NAME: name,
                          ID: steam_id,
                          ELO: elo_1v1,
                          ELO_TG: elo_tg}
            self.df = pd.concat([self.df, pd.Series(new_player).to_frame.T], ignore_index=True)
            # self.df.loc[self.df.index.max() + 1] = [name, steam_id, elo_1v1, elo_tg]
        else:
            print("some of the inputs where provided in the wrong format")
            return -1
        print(self.names)

    # allows to delete a player to the database
    def delete_player(self, name: str):
        if name not in self.df[NAME].values:
            print("{name} not found!")
            return -1
        self.df = self.df[self.df[NAME] != name]

    # updates the csv with data previously saved
    def update_csv(self):
        self.df.reset_index().to_csv(self.fileName, index=False)

    # TODO: I'm not sure what game timestamps are meant to be and how do we want to save them. Is "game_timestamps.csv" a simply a list of timestamps? Or is there a table structure in it?
    # adds games to the file containing all the gametimes
    def add_game(self, timestamp):
        with open(self.fileName_timestamps, "a") as timefile:
            timefile.write(str(timestamp) + "\n")

    # TODO: read previous todo
    # checks if a timestamp is already present in the file
    def check_game(self, timestamp):
        timefile = open(self.fileName_timestamps, "r")
        lines = timefile.readlines()
        for line in lines:
            if str(timestamp) in line:
                return True
        return False

    # TODO: what is the goal of this function?
    def all_players_registered(self, steam_id):
        count = 0
        for id in steam_id:
            for i in range(len(self.steam_id)):
                if id == self.steam_id[i]:
                    count += 1
        if count == len(steam_id):
            return True
        else:
            return False
