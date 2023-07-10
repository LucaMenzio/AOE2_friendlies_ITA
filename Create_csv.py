import pandas as pd
import numpy as np
import csv

names = []
steam_ids = []
elo1v1 = []
elotg =[]
CLAN = []
discord_names = []


fileName = "elo_aoe2italia_internal.csv"
with open(fileName) as csvfile_out:
    csvReader = csv.reader(csvfile_out, delimiter=",")
    for i, row in enumerate(csvReader):
        if i != 0:
            names.append(row[1])
            steam_ids.append(row[3])
            CLAN.append(row[4])
            elo1v1.append(1400)
            elotg.append(1400)
            discord_names.append(row[7])

with open(fileName.replace('.csv', '_new.csv'), 'w') as writeFile:
    for i in range(len(names)):
        if i == 0:
            new_row = ",Names,Discord Nick,Steam ID,Elo 1v1, Elo tg"
        else:
            new_row = str(i)+","+names[i]+","+discord_names[i]+","+steam_ids[i]+","+str(elo1v1[i])+","+str(elotg[i])+"\n"
        writeFile.write(new_row)



        