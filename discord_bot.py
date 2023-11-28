import os
import random

from discord.ext import commands, tasks
#from discord.ext.commands import has_permission
import discord
from dotenv import load_dotenv

from modules import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
Elo = Elo_csv.AOE2ItaliaElo("files/elo_aoe2italia_internal_updated_temp.csv")    
rlk = reliclink_API.relicAPI()


message = "Please check if the bot command is used correctly"

#---------------------------------------------------------------------
@bot.command(name='elo1v1', help='Retrieves the 1v1 elo of the specified player name (please use "")')
async def create_team(ctx, player):
    elo = Elo.get_elo1v1(player)
    await ctx.send(f"{player}: {elo} (1v1)")

#---------------------------------------------------------------------
@bot.command(name='elotg', help='Retrieves the tg elo of the specified player name (please use "")')
async def create_team(ctx, player):
    elo = Elo.get_elotg(player)
    if player == "HSL | Loris":
        message = "Il capo non ha Elo, ma l\'Elo ha un capo (scarso, comunque)"
        await ctx.send(message)
        return None
    await ctx.send(f"{player}: {elo} (tg)")


#---------------------------------------------------------------------
@bot.command(name='create_team', help='Creates a balanced team given the players names (e.g. !create_team "ITA | Born to be Brain" "OS | Piero" "ITA | Carma" "OS | Nessuno" )')
async def create_team(ctx, *players):
    if(len(players) % 2 != 0):
        await ctx.send("Check the number of players, it is odd")
    
    team = Elo.balance_teams_internal(players)
    message ="The best combination of players is \n" 
    for i, player in enumerate(players):
        flag = False
        for ctrl in team:
            if ctrl == i: 
                flag = True
        if flag:
            message += "Team 0 \t " + player + " \n"
        else:
            message += "Team 1 \t " + player + "\n"
    await ctx.send(message)
    
#---------------------------------------------------------------------
@bot.command(name='get_matchinfo', help='Retrieves the info about the last match played by the specified player')
async def create_team(ctx, player, n_games):

    steam_ids = []
    results = []
    names = []
    
    in_steam_id = Elo.get_steam_id(player)
    await ctx.send("Retrieving "+str(n_games)+" matches played by "+player+" with steam ID "+in_steam_id)
    message = ""
    steam_ids, names, results = rlk.getMatches(in_steam_id, int(n_games))
    for i in range(len(steam_ids)):
        if i == 0:
            continue
        message = "```"
        message+= "Game number "+str(i)+"\n"
        message+="+---------------------------------------+\n"
        message+="\tPlayer | Result |\n"
        message+="+---------------------------------------+\n"
        for j in range(len(steam_ids[i])):
            won = 'Won' if results[i][j] == 1 else 'Lost'
            message+="\t"+str(names[i][j])+" \t\t "+str(won)+"\n"
        await ctx.send(message+"```")

#---------------------------------------------------------------------
@bot.command(name='balance_lobby', help='Balances the teams in the specified lobby employing the internal tg Elo - e.g. !balance_lobby 254830248')
async def balance_lobby(ctx, lobby_id):
    names = []
    steam_ids = rlk.findLobby_byID(lobby_id)
    if steam_ids == -2:
        await ctx.send("Error, lobby not found")
    if(len(steam_ids) < 4 or len(steam_ids) %2 != 0):
        await ctx.send("Check the number of players, it is odd or there are less than 3 players")
    for j,id in enumerate(steam_ids):
        if(Elo.get_name(id)):
            await ctx.send("The " +str(j)+"-th player is not registered on the database. Please use the !balance_lobby_1v1elo command or add him/her to the database first")
        names.append(Elo.get_name(id))
        
    team = Elo.balance_teams_internal(names)
    if isinstance(team, int):
        await ctx.send("the lobby does not contain the right amount of players")
    else:
        message = ""
        for i in range(len(names)):
            message += names[i] + "\t" + team[i] + "\n"
        await ctx.send("The most balanced combination is:\n")
        await ctx.send(message)

#---------------------------------------------------------------------
@bot.command(name='balance_lobby_1v1', help='Balances the teams in the specified lobby empoying the 1v1 RM Elo  - e.g. !balance_lobby 254830248')
async def balance_lobby_by1v1(ctx, lobby_id):
    elos = []
    team_names = []
    team_elos = []
    steam_ids = rlk.findLobby_byID(lobby_id)
    print(steam_ids)
    if isinstance(steam_ids, int):
        if steam_ids == -2: await ctx.send("The number of players must be greater than 3 and even")
        else: await ctx.send("Could not find the specified lobby")
    else:
        for id in steam_ids:
            name, elos = rlk.getElos(id)
            team_names.append(name)
            team_elos.append(elos[1])
        team = Elo.balance_teams(team_elos)
        if isinstance(team, int):
            await ctx.send("the lobby does not contain the right amount of players")
        else:
            message = ""
            for i in range(len(team_elos)):
                message += team_names[i] + "\t" + team[i] + "\n"
            await ctx.send("The most balanced combination is:\n")
            await ctx.send(message)

#---------------------------------------------------------------------
@bot.command(name='print_csv', help='Shows the database (csv) - for admin only')
@commands.has_permissions(administrator=True)
async def print_csv(ctx):
    max_len = len(Elo.df)
    max_lines = 20
    for i in range(max_len // max_lines):
        output = Elo.df.iloc[i * max_lines: (i + 1) * max_lines].to_string(justify="right")
        await ctx.send(f"```\n{output}\n```")


#---------------------------------------------------------------------
@bot.command(name='add_player', help='Adds a player to the database - e.g. !add_player "Mozzo Infame" "12345666" 800 921 ')
#@has_permission(administrator=True)
async def add_player(ctx, name, steam_id, elo1v1, elotg):
    flag = Elo.add_player(name=name, steam_id=steam_id, elo_1v1=elo1v1, elo_tg=elotg)
    if(flag):
        Elo.update_csv()
        await ctx.send("Player " + name + " added successfully")
    else:
        await ctx.send("There was an issue adding the player, call Loris and Circe (and check the data format)")
        
#---------------------------------------------------------------------
@bot.command(name='delete_player', help='Deletes a player to the database - e.g. !delete_player "nickname" -  for admin only')
#@has_permission(administrator=True)
async def add_player(ctx, name, steam_id, elo1v1, elotg):
    
    if(Elo.delete_player(name,steam_id,elo1v1,elotg)):
        await ctx.send("Player "+ name + " deleted successfully")
    else:
        await ctx.send("There was an issue deleting the player, call Loris and Circe")
  
#---------------------------------------------------------------------
@bot.command(name='get_elosRM', help='Gets current elos in RM')
#@has_permission(administrator=True)
async def get_elosRM(ctx, name):
    await ctx.send(rlk.getElos(Elo.get_steam_id(name)))    
      
bot.run(TOKEN)

'''
#TODO
@bot.listen()
async def on_ready():
    task_loop.start()


@tasks.loop(seconds=4*3600) #four hours seems reasonable
async def auto_update_database():

    n_games = 10 #to be proportioned with the time inserted above 
    search_string = "dito"
    
    #loops over all the players in the database and looks for games 
    #TODO is missing a check on the smurfs, if not all the players are in the database
    for k in range(len(Elo.steam_id)):
    
        steam_id, names, results, gametime = rlk.getMatches_dito(Elo.steam_id[k],n_games,search_string)
        a = 0
    
        #loops on all the games found 
        for i in range(len(steam_id)):
            if i == 0:
                continue
            if(Elo.all_player_registered(steam_id[i])):
                print("Not all the players are present in the database, please add them for this game to be considered")
                continue
            if(Elo.check_game(timestamp=gametime[i-1])):
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
    
    pass
'''