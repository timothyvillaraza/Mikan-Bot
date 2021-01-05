import discord
import requests
from discord.ext import commands
from collections import defaultdict


# Setup Function
def setup(bot):
    bot.add_cog(WordFrequency(bot))


# Cog Class
class WordFrequency(commands.Cog):
    # Initalizer
    def __init__(self, bot):
        self.bot = bot
        self.frequencyMaps = {}  # Use database eventually, username -> FrequencyMap

    # Class Definitions
    class FrequencyMap:
        def __init__(self, username):
            self.username = username
            self.wordFreq = defaultdict(int) # defaultdict(int): Nonexistant keys assigned 0
            self.sortedKeys = None

    # Helper Functions
    def filterMessage(self, message):
        """
        TODO: Handle Request Errors

        www.purgomalum.com

        Filters a message of profanity. Any censored words
        are replaced with '*' equal to the length of the word

        """
        URL = f'https://www.purgomalum.com/service/json'
        PARAMS = {'text': message}
        responce = requests.get(url=URL, params=PARAMS)
        post_data = responce.json()

        return post_data['result']

    def generateWordFrequency(self, author, userInput):
        """

        Take each word in the input and count up it's occurances.
        Returns the author, word frequency dictionary, and descending order keys for the word frequency.

        """

        author_wordFreq = author.wordFreq
        filtered_message = self.filterMessage(userInput.casefold())

        # If a key doesn't exist, add it with a default value of 0
        for word in filtered_message.split():
            # If the current word was not censored (not all '*')
            if word != len(word) * '*':
                author_wordFreq[word] += 1

        # sorted() returns a *list* of key from most freq keys to least freq keys
        sorted_wordFreqKeys = sorted(
            author_wordFreq, key=author_wordFreq.get, reverse=True)

        return author, author_wordFreq, sorted_wordFreqKeys

    def printWordFreq(self, user):
        """

        CONSOLE

        Prints word frequency for a specific user to the console

        """
        print(f'     [Word Count for {user.name}]')
        for currentKey in user.sortedKeys:
            print(f"     {currentKey}: {user.wordFreq[currentKey]}")

        return

    def createWordFreqString(self, user):
        """

        Returns a word frequency string. Used for the discord bot reply.

        """
        word_frequency = ''
        for key in user.sortedKeys:
            word_frequency += (f"     {key}: {user.wordFreq[key]}\n")

        return word_frequency

    # NOTE: functions decorated with @bot.listen recieves 'Message' instances
    # Listen for Messages (Recieves message object)
    # All events will be slow because this function is ran first?
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # Prevents bot from responding to itself
        if message.author == self.bot.user:
            return

        # Look up mentioned user's word frequency
        if message.author in self.frequencyMaps:
            # Existing User: Pull up from database
            mentioned_word_freq = self.frequencyMaps[message.author]
        else:
            # New User: Add to database
            mentioned_word_freq = self.FrequencyMap(message.author)
            self.frequencyMaps.update({message.author: mentioned_word_freq})

        # Create a word frequency map based on the recieved message
        word_frequency = self.generateWordFrequency(mentioned_word_freq, message.content)

        # Update the mentioned_word_freq's word frequency table
        mentioned_word_freq = word_frequency[0]
        mentioned_word_freq.wordFreq = word_frequency[1]
        mentioned_word_freq.sortedKeys = word_frequency[2]

        # DEBUG: Prints frequency map to CONSOLE
        # printWordFreq(author_freq_map)
        # print('\n')

    # NOTE: name_of_variable : type_of_instance is a discord.py conversion feature
    @commands.command()
    async def freq(self, ctx, mentioned_user: discord.Member):
        # If no mention was included in the mention, return.
        # if len(ctx.message.mentions) < 1:
        #     return

        if mentioned_user in self.frequencyMaps:
            # printWordFreq(users[mentioned_user])
            word_frequncy_string = self.createWordFreqString(
                self.frequencyMaps[mentioned_user])

            # Body of Message
            embed_message = discord.Embed(
                title='Word Count',
                color=discord.Color.blue(),
                description=word_frequncy_string
            )

            # Appears at the top of the message
            embed_message.set_author(
                name=mentioned_user.display_name,
                icon_url=mentioned_user.avatar_url)

            await ctx.send(embed=embed_message)

    # TODO: Look up type() vs isinstance()
    @freq.error
    async def freq_error(self, ctx, error):
        """

        Error Handiling for .freq

        """

        # isinstance(incoming_instance, is_instance_this_type)
        if isinstance(error, commands.MissingRequiredArgument):
            print(
                f'freq ERROR: {ctx.author} did not specify which member to look up.'
            )
