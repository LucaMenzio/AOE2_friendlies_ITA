import numpy as np
import csv

from requests import get as GET
from itertools import combinations


#constant for elo calculation
K = 30.

class AOE2ItaliaElo:
    
    def __init__(self):
        
        self.names = []
        self.discord_nick = []
        self.steam_id = []
        self.elo1v1 = []
        self.elotg = []
        
        
        #getting all the info from the csv
        self.fileName = "elo_aoe2italia_internal.csv"
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
    
    #returns the tg elo for a given player name         
    def get_elotg(self, player_name):

        for i, name in enumerate(self.names):
            if(name == player_name):
                return self.elotg[i]        
        return -1

    #returns two teams balanced with respect of the sigle's tg elos
    def balance_teams(self, team_names):
        team_elos = []
        team = [-1,-1,-1]
        
        #checks to avoid shenanigans
        if (len(team_names) % 2 != 0):
            print("Number of players is odd, check it and try again")
            return team
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

    #sets the elo
    def set_elo(self, player_name, new_elo):
            for i in range(len(self.names)):
                if(player_name == self.names[i]):
                    self.elo[i] = new_elo
                    return 1
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
            
            
    #updates the elos in the csv
    # !!! to be called last !!!
    def update_csv(self):
        with open(self.fileName,"w") as csvfile:
            csvfile.write(",Names,Discord Nick,Steam ID,Elo 1v1, Elo tg\n")
            for i in range(len(self.names)):
                csvfile.write(str(i)+","+self.names[i]+","+self.discord_names[i]+","+self.steam_ids[i]+","+str(self.elo1v1[i])+","+str(self.elotg[i])+"\n")
