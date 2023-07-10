import requests
import json
import numpy as np


alert = True

n_games = 1
steam_ids=[]
players_names = []
players_teams = []
ranked = True
match_name = "GL_Null"

'''
with open("aaaaLoris.csv") as csvfile:
    csvReader = csv.reader(csvfile, delimiter=",")
    for i, row in enumerate(csvReader):
        if i == 0: 
            index = row
        else:
            names.append(row[1])
            found.append(row[2])
            steam_ids.append(int(row[3] or 0))
            clans.append(row[4])
'''


steam_ids = [76561197996386232]

for j, steam_id in enumerate(steam_ids):
    if steam_id > 1: #some ids are absent
        resp_matches = requests.get("https://aoe2.net/api/player/matches?game=aoe2de&steam_id=" + str(steam_id) + '&count=' + str(n_games)).json()
    print(resp_matches)
    for i in resp_matches:
        ranked = i.get('ranked')
        match_name = i.get('name')
        print("Match name: " + str(i.get('name')))
        print("was it ranked? " + str(i.get('ranked')))
        print("Players that participated\tTeam")        
        for j in i.get('players'):
            players_names.append(j.get('name'))
            players_teams.append(j.get('team'))
            print(str(j.get('name'))+"\t"+str(j.get('team')))


