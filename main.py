import os
import discord
from discord.ext import commands

# Class Definitions


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
  print(f'  {message.author.name}: {message.content}')

# Test Command
@client.command()
async def test(ctx):
  await ctx.send('A command was recieved by the bot')

@client.command()
async def eli(ctx):
  await ctx.send('Eli? She\'s only the cutest girlfriend around!')

# Run the Client
client.run(os.getenv('TOKEN'))