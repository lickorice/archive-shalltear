import discord
from discord.ext import commands
import asyncio
from data import ldb
import sqlite3

startup_extensions = ["xp", "admin", "economy"]
version = '0.2 alpha'

bot = commands.Bot(command_prefix='d!')
bot.remove_command('help')
lkdb = ldb.LickDB()


@bot.event
@asyncio.coroutine
async def on_ready():
    """Input here what the bot does on startup."""
    print("Shalltear has started.")
    lkdb.init()


@bot.event
async def on_member_join(mbr):
    """Input here what the bot does when a user joins."""
    try:
        lkdb.insertUser(mbr.id)
        print("Successfully registered {}.".format(mbr.name))
    except sqlite3.IntegrityError:
        print("{} is already registered.".format(mbr.name))


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(input())
