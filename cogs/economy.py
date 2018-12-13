import discord, json, datetime, concurrent, random, asyncio, conf
from discord.ext import commands
from data import db_users, db_helper
from utils import msg_utils

config = conf.Config()

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
        print(target_user)
        string = config.MSG_GIL_CHECK if target_user == None else config.MSG_GIL_CHECK2
        a = await msg_utils.get_target_user(ctx, target_user)
        
        if a == None:
            await ctx.send(config.MSG_USER_NOT_FOUND)
            return
        
        user_db = db_users.UserHelper(False)
        user_db.connect()
        gil = user_db.get_user(a.id)["users"]["user_gil"]
        user_db.close()
        await ctx.channel.send(string.format(a.display_name, gil))

    @commands.command()
    async def give(self, ctx, target_user=None, gil="no"):
        """Transfer your gil to another user."""
        a = ctx.message.author
        try: # TODO: Implement integrity check here:
            if int(gil) == "no":
                await ctx.channel.send(config.MSG_INVALID_CMD)
                return
        except ValueError:
            await ctx.channel.send(config.MSG_INVALID_CMD)
            return
        if target_user == None:
            await ctx.channel.send(config.MSG_GIVE_NO_USER.format(a.id))
            return
        b = await msg_utils.get_target_user(ctx, target_user)
        if b.id == a.id or int(gil) <= 0:
            await ctx.channel.send(config.MSG_AM_I_A_JOKE.format(a.id))
            return
        if b == None:
            await ctx.channel.send(config.MSG_USER_NOT_FOUND)
            return

        user_db = db_users.UserHelper(False)
        user_db.connect()
        a_gil = user_db.get_user(a.id)["users"]["user_gil"]
        b_gil = user_db.get_user(b.id)["users"]["user_gil"]
        if a_gil < int(gil):
            await ctx.channel.send(config.MSG_INSUF_GIL)
            user_db.close()
            return
        user_db.add_gil(a.id, -int(gil))
        user_db.add_gil(b.id, int(gil))
        user_db.close()

        await ctx.channel.send(config.MSG_GIVE.format(b.id, gil, a.id))

        
def setup(bot):
    bot.add_cog(Economy(bot))