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

  thisgame = -1 # placeholder value

  # ignore if it's the bot reacting to its own posts
  if user.bot:
    return

  # if someone clicked the green "sign up" checkmark
  if emoji == "✅":
    # first figure out which game object this message connects to
    for game in games.values():
      if game.message.id == message.id: 
        thisgame = game

    # bookmark TODO react to someone signing up
        
    if DEBUG:
      print("Reaction to game: ")
      print(game.text)
    # ignore all other emoji
  else:
    return

# main loop 
@tasks.loop(seconds=10)
async def mainLoop():
  line_data=[]

  # find the channel object based on conf file
  channel = discord.utils.get(bot.get_all_channels(), guild__name=OUTPUTSERVER, name=OUTPUTCHANNEL)

  # read the data file of current games from webserver
  f = urlopen(URLOFLIST)
  ls = f.readlines()

  # for each line of the web data file
  for l in ls:
    # tab split
    line_data = l.decode("UTF-8").split("\\t")     
    # is this a new game? we're checking by comparing the ids in the file to the ids in our local dict
    if not line_data[0] in games:
      # yes, new game
      if DEBUG:
        print("initializing game", line_data)
      # first we create a message object by sending the text to the discord
      message = await channel.send(line_data[1])
      # next post the interactable reaction
      await message.add_reaction('✅')
      # we then store that object inside the game object along with id, and text from web
      g = game.Game(line_data[0], message, line_data[1])
      # store the newly created game object inside the games array, under the key of the game's id
      games[line_data[0]]=g

  # BOOKMARK TODO remove entries that are expired

# initialization routine performed once when the bot starts up
@bot.event
async def on_ready():
  if DEBUG:
    print("starting\n")
  # find our channel, from conf file data
  channel = discord.utils.get(bot.get_all_channels(), guild__name=OUTPUTSERVER, name=OUTPUTCHANNEL)
  # say hello
  await channel.send("Initializing")
  # everything is online and ready. start the main loop process
  mainLoop.start()

# start bot
bot.run(TOKEN)
