import discord
from secrets import *
from discord.ext import commands
import sys, traceback

initial_extensions = [
    "cogs.admin",
    "cogs.core",
    "cogs.economy",
    "cogs.gambling",
    "cogs.memes",
    "cogs.profile",
    "cogs.roles",
    "cogs.shop"
    ]

bot = commands.Bot(command_prefix=commands.when_mentioned_or('s!'))


def main():
    bot.remove_command('help') # Overwrite the default help command.
    for extension in initial_extensions:
        bot.load_extension(extension)


if __name__ == "__main__":
    main()


@bot.event
async def on_ready():

    print(f"\n\nSuccessfully logged in as: {bot.user.name} [ {bot.user.id} ]\ndiscord.py version: {discord.__version__}\n")

    await bot.change_presence(activity=discord.Game(name="s!help"))
    

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN, bot=True, reconnect=True)
