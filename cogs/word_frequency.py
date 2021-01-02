import discord
from discord.ext import commands
from collections import defaultdict


# Setup Function
def setup(client):
    client.add_cog(WordFrequency(client))


# Cog Class
class WordFrequency(commands.Cog):
    # Initalizer
    def __init__(self, client):
        self.client = client
        self.users = dict()  # Use database eventually

    # Class Definitions
    class FrequencyMap:
        def __init__(self, name):
            self.name = name
            self.wordFreq = defaultdict(int)
            self.sortedKeys = None

    # Helper Functions
    def generateWordFrequency(self, author, userInput):
        """

        Take each word in the input and count up it's occurances.
        Returns the author, word frequency dictionary, and descending order keys for the word frequency.

        """

        # defaultdict(int): If a key doesn't exist, add it with a default value of 0
        wordFreq = author.wordFreq
        for word in userInput.casefold().split():
            wordFreq[word] += 1

        # sorted() returns a *list* of key from most freq keys to least freq keys
        sorted_wordFreqKeys = sorted(wordFreq, key=wordFreq.get, reverse=True)

        return author, wordFreq, sorted_wordFreqKeys

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
        word_frequency = f'[Word Count for {user.name}]\n'
        for currentKey in user.sortedKeys:
            word_frequency += (
                f"     {currentKey}: {user.wordFreq[currentKey]}\n")

        return word_frequency

    # NOTE: functions decorated with @client.listen recieves 'Message' instances
    # Listen for Messages (Recieves message object)
    # All events will be slow because this function is ran first?
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # Prevents bot from responding to itself
        if message.author == self.client.user:
            return

        # Look up author_freq_map of message
        if message.author in self.users:
            # Existing User: Pull up from database
            author_freq_map = self.users[message.author]
        else:
            # New User: Add to database
            author_freq_map = self.FrequencyMap(message.author)
            self.users.update({message.author: author_freq_map})

        # Create a word frequency map based on the recieved message
        word_frequency = self.generateWordFrequency(author_freq_map,
                                                    message.content)

        # Update the author_freq_map's word frequency table
        author_freq_map = word_frequency[0]
        author_freq_map.wordFreq = word_frequency[1]
        author_freq_map.sortedKeys = word_frequency[2]

        # DEBUG: Prints frequency map to CONSOLE
        # printWordFreq(author_freq_map)
        # print('\n')

    # NOTE: name_of_variable : type_of_instance is a discord.py conversion feature
    @commands.command()
    async def freq(self, ctx, mentioned_user: discord.Member):
        # If no mention was included in the mention, return.
        # if len(ctx.message.mentions) < 1:
        #     return

        if mentioned_user in self.users:
            # printWordFreq(users[mentioned_user])
            word_frequncy_string = self.createWordFreqString(
                self.users[mentioned_user])
            await ctx.send(word_frequncy_string)

    # TODO: Look up type() vs isinstance()
    # Error handiling specific to freq() command
    @freq.error
    async def freq_error(self, ctx, error):
        # isinstance(incoming_instance, is_instance_this_type)
        if isinstance(error, commands.MissingRequiredArgument):
            print(
                f'ERROR: {ctx.author} did not specify which member to look up.'
            )
