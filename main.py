import discord
from discord.ext import commands

import sys, traceback

initial_extensions = [
    'cogs.admin',
    'cogs.core',
    'cogs.economy',
    'cogs.xp'
    ]

bot = commands.Bot(command_prefix='s!')


def main():
    for extension in initial_extensions:
        bot.load_extension(extension)


if __name__ == '__main__':
    main()


@bot.event
async def on_ready():

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\ndiscord.py version: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='s!help'))
    print(f'Successfully logged in and booted!')


bot.run(input(), bot=True, reconnect=True)
