import os
import random

from discord.ext import commands
import discord
from dotenv import load_dotenv

from pprint import pprint
import rlink_client
from rlink_client.apis.tags import default_api
# Defining the host is optional and defaults to https://aoe-api.reliclink.com
# See configuration.py for a list of all supported configuration parameters.
rlink_configuration = rlink_client.Configuration(
    host="https://aoe-api.reliclink.com"
)

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
@bot.command(name='create_team', help='Creates a balanced team given the players names (ex. !create_team "ITA | Born to be Brain" "OS | Piero" "ITA | Carma" "OS | Nessuno" )')
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

@bot.command(name='get_recent_matches', help='calls reliclink api to get the recent matches of a player')
async def get_recent_matches(ctx, profile_id):
    with rlink_client.ApiClient(rlink_configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        title = 'age2'
        try:
            query_params = {'title': title, 'profile_ids': '[' + str(profile_id) + ']'}
            api_response = api_instance.community_get_recent_match_history(query_params=query_params)
            pprint(api_response)
            await ctx.send(str(list(api_response.body['matchHistoryStats'])[0]['id']))
        except rlink_client.ApiException as e:
            print("Exception when calling DefaultApi->community_get_recent_match_history: %s\n" % e)

bot.run(TOKEN)

