import os
from urllib.request import urlopen
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OUTPUTCHANNEL = os.getenv('OUTPUT_CHANNEL')

bot = commands.Bot(command_prefix='!')

# bookmark. TODO: create a concept of a state for each game, including owner, when it's closing, and players in it.

@bot.command(name='new', help='Generates a personal link to let the bot know you\'re looking for people to play with.')
async def new(ctx):
    await ctx.send("{}, please click this link to register a new game: http://miriku.com/newGame?user={}".format(ctx.message.author.mention, ctx.message.author.id))

@tasks.loop(seconds=10)
async def mainLoop(post):
    f = urlopen("https://miriku.com/list.txt")
    ls = f.readlines()
    output = ""

    # bookmark. TODO: make this be a tokenizer that parses actual content and is statefully aware of whether a game is 
    #   just opening, waiting for players, has enough players now, or is expired

    for l in ls:
      output = output + l.decode('utf-8') + "\n"
    await post.edit(content=output)

# bookmark. TODO: add respone to reaction

@bot.event
async def on_ready():
    post = await OUTPUTCHANNEL.send("Initializing")
    mainLoop.start(post)

bot.run(TOKEN)
