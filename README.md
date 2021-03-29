## About this Discord Bot
A modular Discord bot created for the purpose of practicing Python, version control, and database usage.

This is a personal project to brush up on Python, learn how to use databases, version control, and basic event-driven programming. The bot was created with the intention of hosting it online with a free version repl.it.

## Features
Discord.py allows users to create "cogs" or encapsulated features that have their own separate functionalities and command prefixes.

By default, the command prefix is the "." (period) character.

**Global Commands**

- .clear_db
  - Clears the repl.it database of all it's keys.

**Word Frequency Commands**

Tracks the word frequency in all messages by all users, filters out profanity using the Purgomalum API, then stores it in a database for later usage.

Commands (All commands begin

 - .freq @[target_username]
   - Returns a paginated list of all the unique words a user has sent to the server. Users can react to the left or right arrow emojis to change pages. There are 10 words per page.
