import csv

from modules import *

rlk = reliclink_API.relicAPI()


names = []
steam_ids = []

with open("academy.csv", "r") as in_csvfile:
    csvReader = csv.reader(in_csvfile, delimiter=",")
    for i, row in enumerate(csvReader):
        if i != 0:
            names.append(row[0])
            steam_ids.append(row[1])

with open("academy_updated.csv", "w") as out_csvfile:
    out_csvfile.write("Name,Nickname,steam_id, tg elo, 1v1 elo\n")
    for i, id in enumerate(steam_ids):
        if id != -1:
            nickname, elos = rlk.getElos(id)
        else:
            elos = [-1, -1]
            nickname = names[i]
        out_csvfile.write(
            names[i]
            + ","
            + nickname
            + ","
            + str(id)
            + ","
            + str(elos[0])
            + ","
            + str(elos[1])
            + "\n"
        )
        print(
            names[i]
            + ","
            + nickname
            + ","
            + str(id)
            + ","
            + str(elos[0])
            + ","
            + str(elos[1])
        )
