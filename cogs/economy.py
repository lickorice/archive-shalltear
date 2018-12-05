import discord, json, datetime, concurrent, random, asyncio
from discord.ext import commands
from data import db_users, db_helper
from utils import msg_utils

owner_id = 319285994253975553 # Lickorice

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class EconomyCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g', 'bal', 'money', '$'])
    async def gil(self, ctx, target_user=None):
        """Check your own gil, or another user's gil."""
        string = "**{}**, you currently have **{}** 💰 gil." if target_user != None else "**{}** currently has **{}** 💰 gil."
        a = await msg_utils.get_target_user(ctx, target_user)
        if a == None:
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
        try:
            if int(gil) == "no":
                await ctx.channel.send(msg_strings["str_invalid-cmd"])
                return
        except ValueError:
            await ctx.channel.send(msg_strings["str_invalid-cmd"])
            return
        if target_user == None:
            await ctx.channel.send("<@{}>, please specify a user.".format(a.id))
            return
        b = await msg_utils.get_target_user(ctx, target_user)
        if b.id == a.id or int(gil) <= 0:
            await ctx.channel.send(msg_strings["str_am-i-a-joke"].format(a.id))
            return
        if b == None:
            await ctx.channel.send(msg_strings["str_user-not-found"])
            return

        user_db = db_users.UserHelper(False)
        user_db.connect()
        a_gil = user_db.get_user(a.id)["users"]["user_gil"]
        b_gil = user_db.get_user(b.id)["users"]["user_gil"]
        if a_gil < int(gil):
            await ctx.channel.send(msg_strings["str_insuf-gil"])
            user_db.close()
            return
        user_db.add_gil(a.id, -int(gil))
        user_db.add_gil(b.id, int(gil))
        user_db.close()

        await ctx.channel.send(msg_strings["str_give"].format(b.id, gil, a.id))

        
def setup(bot):
    bot.add_cog(EconomyCog(bot))