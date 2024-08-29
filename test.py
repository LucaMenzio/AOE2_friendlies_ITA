from modules import *

#a = Elo.AOE2ItaliaElo()

#b = reliclink_API.relicAPI()
#print(b.getElos(a.get_steam_id("HSL | Muca")) )

#elos = []
#team_names = []
#team_elos = []
#steam_ids = b.findLobby_byID(255364261)
#print(steam_ids)
#for id in steam_ids:
#    name, elos = b.getElos(id)
#    team_names.append(name)
#    team_elos.append(elos[1])
#print(a.balance_teams(team_elos))

Elo = Elo_csv.AOE2ItaliaElo("files/elo_aoe2italia_internal_updated_temp.csv")
rlk = reliclink_API.relicAPI()




'''
steam_id, names, results, gametime = rlk.getMatches_dito(76561198315152103,20,"dito")
#add some condition to gametime, if it's already in the file containing all the times TODO 

a = 0

#loops on all the games found 
for i in range(len(steam_id)):
    if i == 0:
        continue
    if (Elo.check_game(timestamp=gametime[i-1])):
        print("game already in the database")
        continue
    Elo.add_game(gametime[i]) #adds the game timestamp to the timestamps file
    elos = []
    won = []
    steam_ids = []
    if(len(steam_id[i]) == 2):
        for j in range(len(steam_id[i])):
            print(names[i][j] + " " + str(Elo.get_elo1v1_byId(steam_id[i][j])) + " " + str(results[i][j]))
            elos.append(Elo.get_elo1v1_byId(steam_id[i][j]))
            won.append(results[i][j])
        Elo.update_elo(steam_id[i][0], True, int(Elo.compute_elo(int(elos[0]), int(elos[1]), int(won[0]))))
        Elo.update_elo(steam_id[i][1], True, int(Elo.compute_elo(int(elos[1]), int(elos[0]), int(won[1]))))
    else:
        mean_elo_team1 = 0
        mean_elo_team2 = 0
        for j in range(len(steam_id[i])):
            elos.append(Elo.get_elo1v1_byId(steam_id[i][j]))
            won.append(results[i][j])
            steam_ids.append(steam_id[i][j])
            if results[i][j]:
                mean_elo_team1 += Elo.get_elotg_byId(steam_id[i][j])
            else:
                mean_elo_team2 += Elo.get_elotg_byId(steam_id[i][j])
        for j in range(len(elos)):
            if won[j]:
                Elo.update_elo(steam_ids[j]), False, int(Elo.compute_elo(int(elos[j]), mean_elo_team2, int(won[j])))
            else:
                Elo.update_elo(steam_ids[j]), False, int(Elo.compute_elo(int(elos[j]), mean_elo_team1, int(won[j])))


names = ["JohnBaudelaire", "ITA | Canazzo", "ITA | Born to be Brain", "ITA | Carma", "ITA | Francesco III", "ITA | GoldFish"]
print(a.get_steam_id("NAPS | L'Ammiraglio"))

b = aoe2net_API.Matches()

print(b.look_for_matches(76561197996386232,"ranked"))
'''