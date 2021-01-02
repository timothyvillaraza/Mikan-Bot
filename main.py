import os
from replit import db
import discord
from discord.ext import commands

# Client Instance: All commands will start with '.'
client = commands.Bot(command_prefix='.', case_insensitive=True)

# Load All Cogs
print('Loading cogs...')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]  # File by name without .py extension
        client.load_extension(f'cogs.{cog_name}')
        print(f'    {cog_name} loaded')
print()  # newline


# On Ready Event
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


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
