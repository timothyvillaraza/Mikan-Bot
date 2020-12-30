import os
import discord
from discord.ext import commands
from collections import defaultdict

# Class Definitions
class word_frequency:
    def __init__(self, name):
        self.name = name
        self.wordFreq = defaultdict(int)
        self.sortedKeys = None

############################
# Word Frequency Functions #
############################

#
# Generate Word Frequency
#
# Take each word in the input and count up it's occurances
#
def wordFreqKeys(userInput):
    # defaultdict(int): If a key doesn't exist, add it with a default value of 0
    wordFreq = defaultdict(int)
    for word in userInput.casefold().split():
        wordFreq[word] += 1

    # sorted() returns a *list* of key from most freq keys to least freq keys
    sorted_wordFreqKeys = sorted(wordFreq, key=wordFreq.get, reverse=True)

    return wordFreq, sorted_wordFreqKeys


#
# Print Word Frequency
#
def printWordFreq(wordFreq, sortedKeys):
    print("\n   [Word Count]")
    for currentKey in sortedKeys:
        print("   {}: {}".format(currentKey, wordFreq[currentKey]))

    return


# Client Instance: All commands will start with '.'
client = commands.Bot(command_prefix = '.')

# On Ready Event
@client.event
async def on_ready():
  print(f'Logged in as {client.user}')

# Message Recieved Event
@client.listen('on_message')
async def on_message(message):
  if message.author == client.user:
    return

  # message.author: MafuMafu Tofu
  # message.author.name: MafuMafu Tofu
  # message.author.display_name/.nick = Tim
  print(f'  {message.author.author}: {message.content}')

# Test Command
@client.command()
async def test(ctx):
  await ctx.send('A command was recieved by the bot')

@client.command()
async def eli(ctx):
  await ctx.send('Eli? She\'s only the cutest girlfriend around!')

# Run the Client
client.run(os.getenv('TOKEN'))