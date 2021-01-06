import os
import discord
from replit import db
from discord.ext import commands

# bot Instance: All commands will start with '.'
bot = commands.Bot(command_prefix='.', case_insensitive=True)

# Load All Cogs
print('Loading cogs...')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]  # File by name without .py extension
        bot.load_extension(f'cogs.{cog_name}')
        print(f'    {cog_name} loaded')
print()  # newline


# On Ready Event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def clear_db(ctx):
    """

    Clears all keys in the repl.it database

    """
    
    await ctx.send('Clearing all database keys.')

    for key in db:
        print(f'{key} deleted')
        del db[key]

    await ctx.send('All keys in the database deleted.')


# Run the bot
bot.run(os.getenv('TOKEN'))
