import os
from replit import db
import discord
from discord.ext import commands

# Client Instance: All commands will start with '.'
client = commands.Bot(command_prefix='.')


# On Ready Event
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


# Load All Cogs
for filename in os.listdir('./cogs'):
    # If the current file ends in .py
    if filename.endswith('.py'):
        # Load the file by name (without .py)
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
async def clear_db(ctx):
    """
    
    Clears all keys in the repl.it database

    """
    await ctx.send('Clearing all database keys.')

    for key in db:
        print(f'{key} deleted')
        del db[key]

    await ctx.send('All keys in the database deleted.')


# Run the Client
client.run(os.getenv('TOKEN'))
