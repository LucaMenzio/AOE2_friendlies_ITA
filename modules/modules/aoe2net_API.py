import requests

#constants for matches search
MATCHNAME = "ranked"
N_OF_MATCHES = 10


class Matches:
    
    def __init__(self):
        self.players_teams = []
        self.players_names = []
        
    def look_for_matches(self, steam_id, match_name="ranked"):
        result = 1
        #to be implemented with a new api for match searching
        resp_matches = requests.get("https://aoe2.net/api/player/matches?game=aoe2de&steam_id=" + str(steam_id) + '&count=' + str(N_OF_MATCHES)).json()
        for i in resp_matches:
            if(i.get('ranked') == "True"):
                continue
            match_name = i.get('name')  
            for j in i.get('players'):
                self.players_names.append(j.get('name'))
                self.players_teams.append(j.get('team'))
            if(len(self.players_names))>2:
                print("found tg")
            else:
                print("found 1v1")
            return self.players_names, self.players_teams, result, match_name
        