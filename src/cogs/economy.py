import discord, json, datetime, concurrent, random, asyncio
from conf import *
from discord.ext import commands
from data import db_users, db_helper
from utils import msg_utils
from objects.user import User

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Economy:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g', 'bal', 'balance', 'money', '$'])
    async def gil(self, ctx, target_user: discord.Member=None):
        """Check your own gil, or another user's gil."""
        if target_user == None:
            target_user = ctx.author

        string = MSG_GIL_CHECK if target_user == None else MSG_GIL_CHECK2
        await ctx.channel.send(string.format(
            target_user.display_name, User(target_user.id).gil))

    @commands.command()
    @commands.guild_only()
    async def give(self, ctx, target_user: discord.Member, gil: int):
        """Transfer your gil to another user."""
        a = ctx.message.author
        b = target_user
        if b.id == a.id or gil <= 0:
            await ctx.channel.send(MSG_AM_I_A_JOKE.format(a.id))
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