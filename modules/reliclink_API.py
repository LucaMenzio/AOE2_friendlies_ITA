import requests
import json
import numpy as np

class relicAPI:

    def __init__(self):
        
        self.steam_id = [[]]
        self.names = [[]]
        self.results = [[]]
    
    #gives back info regarding a certain match(es) found with some player steam_id
    def getMatches(self, in_steam_id, n_matches):
        
        a = 0
        profile_ids = []
        steam_id = []
        names = []
        results = []
        
        resp_matches = requests.get("https://aoe-api.reliclink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22%2Fsteam%2F"+str(in_steam_id)+"%22]").json()

        for matches_history in resp_matches.get('matchHistoryStats'):
            
            steam_id.clear()
            names.clear()
            results.clear()
            profile_ids.clear()
            
            for members in matches_history.get('matchhistoryreportresults'):
                profile_ids.append(members.get('profile_id'))
                results.append(members.get('resulttype'))

            for id in profile_ids:
                for prf in resp_matches.get('profiles'):
                    if prf.get('profile_id') == id:
                        steam_id.append(prf.get('name').replace("/steam/",""))
                        names.append(prf.get('alias'))
                        break
                    
            self.steam_id.append(steam_id)
            self.names.append(names)
            self.results.append(results)
            
            a +=1 
            if a == n_matches:
                return self.steam_id, self.names, self.results
        return -1