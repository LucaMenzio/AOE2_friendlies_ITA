import numpy as np
import csv

from requests import get as GET
from itertools import combinations


#constant for elo calculation
K = 30.

class AOE2ItaliaElo:
    
    def __init__(self, fileName):
        
        self.names = []
        self.discord_nick = []
        self.steam_id = []
        self.elo1v1 = []
        self.elotg = []
        
        
        #getting all the info from the csv
        self.fileName = fileName
        with open(self.fileName) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=",")
            for i, row in enumerate(csvReader):
                if i != 0:
                    self.names.append(row[1])
                    self.discord_nick.append(row[2])
                    self.steam_id.append(row[3])
                    self.elo1v1.append(row[4])
                    self.elotg.append(row[5])
                    
    
    #returns the 1v1 elo for a given player name 
    def get_elo1v1(self, player_name):
        for i, name in enumerate(self.names):
            if(name == player_name):
                return self.elo1v1[i]
        return -1
    
    #returns the 1v1 elo for a given player steam id 
    def get_elo1v1_byId(self, player_steam_id):
        for i, id in enumerate(self.steam_id):
            if(id == player_steam_id):
                return self.elo1v1[i]
        return -1
    
    #returns the tg elo for a given player name         
    def get_elotg(self, player_name):
        for i, name in enumerate(self.names):
            if(name == player_name):
                return self.elotg[i]        
        return -1

    #returns the tg elo for a given player name         
    def get_elotg_byId(self, player_steam_id):
        for i, id in enumerate(self.steam_id):
            if(id == player_steam_id):
                return self.elotg[i]
        return -1

    #returns two teams balanced with respect of the sigle's tg elos
    def balance_teams_internal(self, team_names):
        difference = 1000
        team_elos = []
        team = [-1,-1,-1]
        
        #checks to avoid shenanigans
        if (len(team_names) % 2 != 0):
            print("Number of players is odd, check it and try again")
            return -1
        else:
            if(len(team_names) == 2):
                print("No need for balancing here")
                return team
            #finished with checks
            else:
                #takes the elo of the matching names
                for team_name in team_names:
                    for i, name in enumerate(self.names):
                        if team_name == name:
                            team_elos.append(self.elotg[i])
                if len(team_elos) != len(team_names):
                    print("Did not found some names, please be precise")
                    return team
                
                #starting actual team balancing
                team.clear()        
                n = len(team_names)
                team_elos = [int(elo) for elo in team_elos]
                sum_elo = np.sum(np.array(team_elos))
                possible_combinations = list(combinations(range(n),int(n/2)))
                for i in range(len(possible_combinations)):
                    sum = 0
                    for j in range(int(n/2)):
                        sum += team_elos[possible_combinations[i][j]]

                    if difference > np.abs(sum - sum_elo/2):
                        good_i = i
                        difference = np.abs(sum - sum_elo/2)
                team = possible_combinations[good_i]
                
                return team
    
    #balances the teams by providing the elos only
    def balance_teams(self, elos):
        difference = 1000
        team = [-1,-1,-1]
        if (len(elos) % 2 != 0):
            print("Number of players is odd, check it and try again")
            return -1
        if(len(elos) == 2):
            print("No need for balancing")
            return -2
        team.clear()
        n = len(elos)
        print(elos)
        sum_elo = np.sum(np.array(elos))
        possible_combinations = list(combinations(range(n),int(n/2)))
        for i in range(len(possible_combinations)):
            sum = 0
            for j in range(int(n/2)):
                sum += elos[possible_combinations[i][j]]
            if (difference > np.abs(sum - sum_elo/2) ):
                good_i = i
                difference = np.abs(sum - sum_elo/2)
            team = possible_combinations(good_i)
        return team

    #sets the elo
    def set_elo(self, player_name, new_elo):
            for i in range(len(self.names)):
                if(player_name == self.names[i]):
                    self.elo[i] = new_elo
                    return 1
            return -1
        
    #gets the player nickname given a certain steam id
    def get_name(self, player_steam_id):
        for i in range(len(self.names)):
            if(self.steam_id == player_steam_id):
                return self.names[i]
        return -1
    
    #gets the steam id corresponding to a certain player name
    def get_steam_id(self, player_name):
        for i in range(len(self.names)):
            if(player_name == self.names[i]):
                return self.steam_id[i]
        return -1
    
    #computes the new elo of p1, assuming constant K 
    def compute_elo(self, elo_p1, elo_p2, won):
        p1 = 1.0 / (1.0 + np.power(10, (elo_p2 - elo_p1)/400) )
        return elo_p1 + K*(won - p1)
    
    #updates the elo of the specified player (by steam_id)
    def update_elo(self, steam_id, is_1v1, new_elo):
        for i in range(len(self.names)):
            if self.steam_id[i] == steam_id:
                if is_1v1:
                    print("updated 1v1 elo, new elo is " + str(new_elo))
                    self.elo1v1[i] = new_elo
                else:
                    self.elotg[i] = new_elo
        #TOTEST
        
    
    #allows to add a player to the database
    def add_player(self, name, steam_id, elo_1v1, elo_tg):
        if isinstance(name, str) and isinstance(steam_id, str) and isinstance(elo_1v1, int) and isinstance(elo_tg, int):
            self.names.append(name)
            self.discord_nick.append(name)
            self.steam_id.append(steam_id)
            self.elo1v1.append(elo_1v1)
            self.elotg.append(elo_tg)
        else:
            print("some of the inputs where provided in the wrong format")
            return -1
    
    #allows to add a player to the database
    def delete_player(self, name):
        j = 0
        for i in range(len(self.names)):
            if j == len(self.names):
                break
            if name == self.names[i]:
                j += 1
                continue
            self.names[i] = self.names[j]
            self.steam_id[i] = self.steam_id[j]
            self.elo1v1[i] = self.elo1v1[j]
            self.elotg[i] = self.elotg[j]
            self.discord_nick[i] = self.discord_nick[j] 
            j += 1
    
    
    #updates the csv with data previously saved
    def update_csv(self):
        with open(self.fileName,"w") as csvfile:
            csvfile.write(",Names,Discord Nick,Steam ID,Elo 1v1, Elo tg\n")
            for i in range(len(self.names)):
                csvfile.write(str(i)+","+self.names[i]+","+self.discord_nick[i]+","+self.steam_id[i]+","+str(self.elo1v1[i])+","+str(self.elotg[i])+"\n")
        print("Database Updated successfully")       
    