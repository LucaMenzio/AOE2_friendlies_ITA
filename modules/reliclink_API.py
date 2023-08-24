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
    
    def getMatches(self, in_steam_id, n_matches, search_string):
        
        a = 0
        profile_ids = []
        steam_id = []
        names = []
        results = []
        
        try:
            resp_matches = requests.get("https://aoe-api.reliclink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22%2Fsteam%2F"+str(in_steam_id)+"%22]").json()

            for matches_history in resp_matches.get('matchHistoryStats'):

                if not ( search_string in matches_history.get("description") ):     # or matches_history.get("description").contains("DITO") or matches_history.get("description").contains("Dito"))
                    a +=1 
                    continue
                else:
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
                    break
        except:
            return -1

    #returnes the 1v1 elo or -1 if it is not found
    def getElos(self, in_steam_id):
        
        try:
            resp_profile = requests.get("https://aoe-api.reliclink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22%2Fsteam%2F" + str(in_steam_id) + "%22]").json()
            #print("gettiong elo of player " + str(resp_profile.get("statGroups")))

            a = 0 #used to quit the scrolling after saving 1v1 and tg data
            elos = []
            for stats in resp_profile.get("leaderboardStats"):
                if a > 1:
                    break
                #print(stats.get("rating"))
                elos.append(stats.get("rating"))
                a += 1
            for stats in resp_profile.get("statGroups"):
                for i in stats.get("members"):
                    name = i.get("alias")
            return name, elos #first one is RM 1v1 elo, second RM tg elo
        except:
            return -1
    
    #returns the players steam ids in lobbies selected by id
    def findLobby_byID(self, lobby_id):
        players_id = []
        steam_id = []
        try:
            resp_lobby = requests.get("https://aoe-api.reliclink.com/community/advertisement/findAdvertisements?title=age2").json()
            for lobby in resp_lobby.get("matches"):
                #lobby_title = lobby.get("description")
                #if (" dito" in lobby_title) or ("dito " lobby_title) or (" DITO" in lobby_title) or "DITO " in lobby_title:
                if lobby_id == lobby.get("id"):
                    for i in lobby.get("matchmembers"):
                        players_id.append(i.get("profile_id"))

            if len(players_id) > 3:
                for id in players_id:
                    for avatar in resp_lobby.get("avatars"):
                        if(avatar.get("profile_id") == id):
                            steam_id.append(avatar.get('name').replace("/steam/",""))
                return steam_id
            else:
                return -2 #less than 3 players in lobby
        except:
            print("No lobbies found - Error")
            return -1 