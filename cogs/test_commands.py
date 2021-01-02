import discord
from discord.ext import commands


# Setup
def setup(client):
    client.add_cog(TestCommands(client))


# All 'Context' instances have a 'Message' instance
    # 'Message' instances
    # message.content: The sent message
    # message.author: MafuMafu Tofu#3910
    # message.author.name: MafuMafu Tofu
    # message.author.display_name/.nick = Tim
    # print(f'  {message.author}: {message.content}')


# Cog Class
class TestCommands(commands.Cog):
    # Initalizer
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def eli(self, ctx):
        await ctx.send('Eli? She\'s only the cutest girl around!')

    # Test Mention
    @commands.command()
    async def test(self, ctx):
        test = ctx.author
        await ctx.send(f'{test}')

    # NOTE: functions decorated with @commands.command recieves 'Context' instances
    # Test Mention
    @commands.command()
    async def mention(self, ctx, mentioned_user: discord.Member):
        await ctx.send(f'{mentioned_user}')
        