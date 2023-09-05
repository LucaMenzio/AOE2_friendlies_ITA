from modules import *

a = Elo.AOE2ItaliaElo()

b = reliclink_API.relicAPI()
print(b.getElos(a.get_steam_id("HSL | Muca")) )

flag = False
with open("elo_aoe2italia_internal_updated_temp.csv", "w") as csvfile:
    csvfile.write(",Names,Discord Nick,Steam ID,Elo 1v1, Elo tg\n")
    for i in range(len(a.names)):
        flag = False
        if(a.steam_id[i] != -1):
            elos = []
            elos = b.getElos(a.steam_id[i])
            if isinstance(elos, list): 
                if len(elos) == 2:
                    flag = True
           
        if flag:
            print(elos)
            csvfile.write(str(i)+","+a.names[i]+","+a.discord_nick[i]+","+str(a.steam_id[i])+","+str(elos[0])+","+str(elos[1])+"\n")
        else:
            csvfile.write(str(i)+","+a.names[i]+","+a.discord_nick[i]+","+str(a.steam_id[i])+","+str(a.elo1v1[i])+","+str(a.elotg[i])+"\n")
            print("there was an issue with player "+a.names[i])