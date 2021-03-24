import os
import game
import discord
from urllib.request import urlopen
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OUTPUTCHANNEL = os.getenv('OUTPUT_CHANNEL')
WEBSITESTRING = os.getenv('WEBSITE_STRING')
URLOFLIST = os.getenv('URL_OF_DATA_FILE')
DEBUG = os.getenv('DEBUG_LEVEL')

bot = commands.Bot(command_prefix='!')

# bot's state
games = {}

# helper command: link to website with message
@bot.command(name='new', help='Generates a personal link to let the bot know you\'re looking for people to play with.')
async def new(ctx):
  await ctx.send("{}, please click this link to register a new game: {}{}".format(ctx.message.author.mention, WEBSITESTRING, ctx.message.author.id))

# main loop 
@tasks.loop(seconds=10)
async def mainLoop():
  f = urlopen(URLOFLIST)
  ls = f.readlines()

  for l in ls:
    line_data = l.split(b"\t")     
    # is this a new game?
    if not line_data[0] in games:
      if DEBUG:
        print("initializing game" + str(line_data[0]))
      # add it, first create a game object
      g = game.Game(line_data[0])
      games[line_data[0]]=g

# performed once when the bot starts up
@bot.event
async def on_ready():
  if DEBUG:
    print("starting\n")
  channel = discord.utils.get(bot.get_all_channels(), guild__name='IRC Boardgames', name='bots')
  await channel.send("Initializing")

mainLoop.start()
bot.run(TOKEN)
