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

    @commands.command(aliases=['ltpot'])
    async def lotterypot(self, ctx):
        """This shows the current lottery jackpot."""
        helper_db = db_helper.DBHelper("data/db/misc.db", False)
        helper_db.connect()
        try:
            current_pot = helper_db.fetch_rows(
                "lottery", strict=True,
                guild_id=ctx.guild.id
            )[0]["pot_amount"]
        except IndexError:
            helper_db.insert_row("lottery", guild_id=ctx.guild.id, pot_amount=0)
            current_pot = 0
        await ctx.channel.send(msg_strings["str_lottery-pot"].format(current_pot))

    @commands.command(aliases=['lt'])
    @commands.cooldown(2, 10, type=commands.BucketType.user)
    async def lottery(self, ctx, number=None):
        """Take your chances with the lottery!"""

        author = ctx.message.author

        user_db = db_users.UserHelper(False)
        user_db.connect()
        gil = user_db.get_user(author.id)["users"]["user_gil"]

        if gil <= 2:
            await ctx.channel.send(msg_strings["str_insuf-gil"])
            user_db.close()
            return

        def check(m):
            try:
                return author.id == m.author.id and 0<=int(m.content)<=999
            except:
                return False

        if number==None:
            await ctx.channel.send(msg_strings["str_lottery-no"].format(author.display_name))
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=10)
            except concurrent.futures._base.TimeoutError:
                await ctx.channel.send(msg_strings["str_timeout"].format(author.id))
            lottery_entry = int(msg.content)
        else:
            try:
                lottery_entry = int(number)
            except ValueError:
                await ctx.channel.send(msg_strings["str_invalid-cmd"])

        # generate lottery:
        numdict = {1:"one", 2:"two", 3: "three", 4:"four",
        5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine", 0:"zero"}
        string = [i for i in "❓❓❓"]
        msg = await ctx.channel.send(''.join(string))
        num_total = 0
        for i in range(3):
            current_number = random.randint(0, 9)
            string[i] = ':{}:'.format(numdict[current_number])
            await msg.edit(content=''.join(string))
            num_total += current_number*(10**(2-i))

        if num_total == lottery_entry:
            helper_db = db_helper.DBHelper("data/db/misc.db", False)
            helper_db.connect()
            try:
                current_pot = helper_db.fetch_rows(
                    "lottery", strict=True,
                    guild_id=ctx.guild.id
                )[0]["pot_amount"] + 2
            except IndexError:
                helper_db.insert_row("lottery", guild_id=ctx.guild.id, pot_amount=0)
                current_pot = 2
            helper_db.update_column("lottery", "pot_amount", 0, guild_id=ctx.guild.id)
            helper_db.close()

            await ctx.channel.send(msg_strings["str_lottery-win"].format(author.id, current_pot))

            user_db = db_users.UserHelper(False)
            user_db.connect()
            user_db.add_gil(author.id, current_pot)
            user_db.close()
        else:
            user_db = db_users.UserHelper(False)
            user_db.connect()
            user_db.add_gil(author.id, -2)
            user_db.close()

            helper_db = db_helper.DBHelper("data/db/misc.db", False)
            helper_db.connect()
            try:
                current_pot = helper_db.fetch_rows(
                    "lottery", strict=True,
                    guild_id=ctx.guild.id
                )[0]["pot_amount"]
                helper_db.update_column("lottery", "pot_amount", current_pot+2, guild_id=ctx.guild.id)
            except IndexError:
                helper_db.insert_row("lottery", guild_id=ctx.guild.id, pot_amount=2)
            helper_db.close()
            await ctx.channel.send(msg_strings["str_lottery-loss"].format(author.display_name))
            

        
def setup(bot):
    bot.add_cog(EconomyCog(bot))