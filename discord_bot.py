import os
import random

from discord.ext import commands
import discord
from dotenv import load_dotenv

from modules import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
Elo = Elo.AOE2ItaliaElo()    

message = "Please check if the bot command is used correctly"

#
@bot.command(name='roll_dice', help='Simulates rolling dice. Wants the number of the dice and its sides as arguments')
async def roll(ctx, number_of_dice, number_of_sides):
    dice = [
        str(random.choice(range(1, int(number_of_sides) + 1)))
        for _ in range(int(number_of_dice))
    ]
    await ctx.send(', '.join(dice))
#---------------------------------------------------------------------

#
@bot.command(name='elo1v1', help='Retrieves the 1v1 elo of the specified player name (please use "")')
async def create_team(ctx, player):
    message = str(Elo.get_elo1v1(player))
    await ctx.send(message)

#
@bot.command(name='elotg', help='Retrieves the tg elo of the specified player name (please use "")')
async def create_team(ctx, player):
    message = str(Elo.get_elotg(player))
    await ctx.send(message)

#
@bot.command(name='create_team', help='Creates a balanced team given the players names (ex. !create_team "ITA | Born to be Brain" "OS | Piero" "ITA | Carma" "OS | Nessuno" )')
async def create_team(ctx, *players):
    if(len(players) %2 != 0):
        await ctx.send("Check the number of players, it is odd")
        
    team = Elo.balance_teams(players)
    message ="The best combination of players is " + str(team)
    await ctx.send(message)


'''
#
@bot.command(name='matchinfo', help='Retrieves the info about the matches played by the specified player')
async def create_team(ctx, player):

    await ctx.send(message)
'''

bot.run(TOKEN)
