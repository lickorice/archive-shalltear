# import discord
# from discord.ext import commands
# import asyncio
# from data import ldb
# import sqlite3

# startup_extensions = ["xp", "admin", "economy", "shop", "memes", "gacha"]
# version = '0.5 alpha'

# bot = commands.Bot(command_prefix='s!')
# bot.remove_command('help')
# lkdb = ldb.LickDB()


# @bot.event
# @asyncio.coroutine
# async def on_ready():
#     """Input here what the bot does on startup."""
#     print("{} has started.".format(bot.user.name))
#     lkdb.init()


# @bot.event
# async def on_member_join(mbr):
#     """Input here what the bot does when a user joins."""
#     try:
#         lkdb.insertUser(mbr.id)
#         print("Successfully registered {}.".format(mbr.name))
#     except sqlite3.IntegrityError:
#         print("{} is already registered.".format(mbr.name))


# if __name__ == '__main__':
#     for extension in startup_extensions:
#         try:
#             bot.load_extension(extension)
#         except Exception as e:
#             exc = '{}: {}'.format(type(e).__name__, e)
#             print('Failed to load extension {}\n{}'.format(extension, exc))
#     bot.run(input())

import discord
from discord.ext import commands

import sys, traceback

initial_extensions = [
    'cogs.admin',
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