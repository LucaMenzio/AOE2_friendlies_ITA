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
Elo = Elo.AOE2ItaliaElo()    
rlk = reliclink_API.relicAPI()


message = "Please check if the bot command is used correctly"

# first attempt to make a bot command, found online
@bot.command(name='roll_dice', help='Simulates rolling dice. Wants the number of the dice and its sides as arguments')
async def roll(ctx, number_of_dice, number_of_sides):
    dice = [
        str(random.choice(range(1, int(number_of_sides) + 1)))
        for _ in range(int(number_of_dice))
    ]
    await ctx.send(', '.join(dice))
#---------------------------------------------------------------------

#---------------------------------------------------------------------
@bot.command(name='elo1v1', help='Retrieves the 1v1 elo of the specified player name (please use "")')
async def create_team(ctx, player):
    message = str(Elo.get_elo1v1(player))
    await ctx.send(message)

#---------------------------------------------------------------------
@bot.command(name='elotg', help='Retrieves the tg elo of the specified player name (please use "")')
async def create_team(ctx, player):
    message = str(Elo.get_elotg(player))
    if player == "HSL | Loris":
        message = "Il capo non ha Elo, ma l\'Elo ha un capo (scarso, comunque)"
    await ctx.send(message)

#---------------------------------------------------------------------
@bot.command(name='create_team', help='Creates a balanced team given the players names (e.g. !create_team "ITA | Born to be Brain" "OS | Piero" "ITA | Carma" "OS | Nessuno" )')
async def create_team(ctx, *players):
    if(len(players) %2 != 0):
        await ctx.send("Check the number of players, it is odd")
        
    team = Elo.balance_teams(players)
    message ="The best combination of players is " + str(team)
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
    message = "The most balanced sets of players are " + str(team)
    await ctx.send(message)

#---------------------------------------------------------------------
@bot.command(name='balance_lobby_1v1', help='Balances the teams in the specified lobby empoying the 1v1 RM Elo  - e.g. !balance_lobby 254830248')
async def balance_lobby_by1v1(ctx, lobby_id):
    elos = []
    team_names = []
    team_elos = []
    steam_ids = rlk.findLobby_byID(lobby_id)
    for id in steam_ids:
        name, elos = rlk.getElos(id)
        team_names.append(name)
        team_elos.append(elos[1])
    team = Elo.balance_teams(team_elos)
    message = ""
    for i in range(len(team_elos)):
        message += name + "\t" + team[i] + "\n"
    await ctx.send("The most balanced combination is:\n")
    await ctx.send(message)

#---------------------------------------------------------------------
@bot.command(name='print_csv', help='Shows the database (csv) - for admin only')
@commands.has_permissions(administrator=True)
async def print_csv(ctx):
    message = ""
    await ctx.send("Names\tDiscord Nick\tSteam ID\tElo 1v1\tElo tg")
    for i in range(len(Elo.names)):
        message += str(Elo.names[i]) + "\t" + str(Elo.discord_nick[i]) + "\t" + str(Elo.steam_id[i]) + "\t" + str(Elo.elo1v1[i]) + "\t" + str(Elo.elotg[i]) + "\n"
        if i % 20 == 0:
            await ctx.send(message)
            message = ""
        if i == len(Elo.names) -1:
            await ctx.send(message)
    

#---------------------------------------------------------------------
@bot.command(name='add_player', help='Adds a player to the database - e.g. !add_player "nickname" "steam id" "1v1 Elo" "tg Elo" ')
async def add_player(ctx, name, steam_id, elo1v1, elotg):
    
    if(Elo.add_player(name,steam_id,elo1v1,elotg)):
        await ctx.send("Player "+ name + " added successfully")
    else:
        await ctx.send("There was an issue adding the player, call Loris and Circe")
        
#---------------------------------------------------------------------
@bot.command(name='delete_player', help='Deletes a player to the database - e.g. !delete_player "nickname" -  for admin only')
#@has_permission(administrator=True)
async def add_player(ctx, name, steam_id, elo1v1, elotg):
    
    if(Elo.delete_player(name,steam_id,elo1v1,elotg)):
        await ctx.send("Player "+ name + " deleted successfully")
    else:
        await ctx.send("There was an issue deleting the player, call Loris and Circe")
    
bot.run(TOKEN)

'''
@bot.listen()
async def on_ready():
    task_loop.start()

@tasks.loop(seconds=5.0)
async def task_loop():
    #TODO
    pass
'''