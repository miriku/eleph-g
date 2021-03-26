import os
import game
import discord
import time
from urllib.request import urlopen
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OUTPUTSERVER = os.getenv('OUTPUT_SERVER')
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

# respond to reaction
#  - first let the website know that a new person joined
#  - then if it's full, message everyone
@bot.event
async def on_reaction_add(reaction, user):
  emoji = reaction.emoji
  message = reaction.message
  thisgame = ""

  if user.bot:
    return

  if emoji == "✅":
    thisGame=-1
    for game in games.values():
      if game.message.id == message.id: 
        thisgame = game
        
    if DEBUG:
      print("Reaction to game:  ")
      print(game.text)
  else:
    return

# main loop 
@tasks.loop(seconds=10)
async def mainLoop():
  channel = discord.utils.get(bot.get_all_channels(), guild__name=OUTPUTSERVER, name=OUTPUTCHANNEL)
  f = urlopen(URLOFLIST)
  ls = f.readlines()
  line_data=[]

  for l in ls:
    line_data = l.decode("UTF-8").split("\\t")     
    # is this a new game?
    if not line_data[0] in games:
      if DEBUG:
        print("initializing game", line_data)
      # add it, first create a game object
      message = await channel.send(line_data[1])
      emoji = '✅'
      await message.add_reaction(emoji)
      g = game.Game(line_data[0], message, line_data[1])
      games[line_data[0]]=g

  # BOOKMARK TODO remove entries that are expired

# performed once when the bot starts up
@bot.event
async def on_ready():
  if DEBUG:
    print("starting\n")
  channel = discord.utils.get(bot.get_all_channels(), guild__name=OUTPUTSERVER, name=OUTPUTCHANNEL)
  await channel.send("Initializing")
  mainLoop.start()

bot.run(TOKEN)
