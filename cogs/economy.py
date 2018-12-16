import discord, json, datetime, concurrent, random, asyncio
from conf import *
from discord.ext import commands
from data import db_users, db_helper
from utils import msg_utils
from objects.user import User

# TODO: Test all commands to check if config migration is a success.

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Economy:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g', 'bal', 'money', '$'])
    async def gil(self, ctx, target_user=None):
        """Check your own gil, or another user's gil."""
        string = MSG_GIL_CHECK if target_user == None else MSG_GIL_CHECK2
        a = await msg_utils.get_target_user(ctx, target_user)
        
        if a == None:
            await ctx.send(MSG_USER_NOT_FOUND)
            return
        
        await ctx.channel.send(string.format(
            a.display_name, User(a.id).gil))

    @commands.command()
    async def give(self, ctx, target_user, gil):
        """Transfer your gil to another user."""
        a = ctx.message.author
        try: # TODO: Implement integrity check here:
            gil = int(gil)
        except ValueError:
            await ctx.channel.send(MSG_INVALID_CMD)
            return
        b = await msg_utils.get_target_user(ctx, target_user)
        if b.id == a.id or gil <= 0:
            await ctx.channel.send(MSG_AM_I_A_JOKE.format(a.id))
            return
        if b == None:
            await ctx.channel.send(MSG_USER_NOT_FOUND)
            return

        _a = User(a.id)
        _b = User(b.id)

        if _a.gil < int(gil):
            await ctx.channel.send(MSG_INSUF_GIL)
            return
        _a.add_gil(-gil)
        _b.add_gil(gil)

        await ctx.channel.send(MSG_GIVE.format(b.id, gil, a.id))

        
def setup(bot):
    bot.add_cog(Economy(bot))