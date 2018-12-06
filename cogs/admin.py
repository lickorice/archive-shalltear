import discord, json, datetime, conf
from discord.ext import commands
from data import db_users

config = conf.Config()

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Administration:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['k'])
    async def kill(self, ctx):
        """Logout command (Owner)."""
        if ctx.author.id == config.OWNER_ID:
            await self.bot.logout()
        else:
            await ctx.channel.send(msg_strings["str_insuf-perms"])

    @commands.command()
    async def registerall(self, ctx):
        """Adds all users (Owner)."""
        if ctx.author.id != config.OWNER_ID:
            await ctx.channel.send(msg_strings["str_insuf-perms"])
        user_db = db_users.UserHelper()
        if not user_db.connect():
            log("[-ERR-] Database failed to connect.")
        reg_count, bot_count, all_count = 0, 0, 0
        for member in self.bot.get_all_members():
            if not member.bot:
                user_db.new_user(member.id)
                reg_count += 1
            else:
                bot_count += 1
            all_count += 1
        user_db.close()

        await ctx.channel.send(
            msg_strings["str_register-3"].format(all_count, reg_count, bot_count)
            )
    
    @commands.command(aliases=['gb'])
    async def grantbadge(self, ctx, item_id):
        """Grants a badge (Owner)."""
        if ctx.message.author.id != config.OWNER_ID:
            return
        user_db = db_users.UserHelper()
        user_db.connect()
        user_db.add_item(ctx.message.author.id, int(item_id))
        user_db.close()

    @commands.command(aliases=['gg'])
    async def grantgil(self, ctx, gil_amount):
        """Grants all users Gil (Owner)."""
        if ctx.message.author.id != config.OWNER_ID:
            return
        user_db = db_users.UserHelper()
        user_db.connect()
        for member in self.bot.get_all_members():
            if not member.bot:
                user_db.add_gil(member.id, int(gil_amount))
        user_db.close()
        send_str = 'str_grant-all-positive' if int(gil_amount) > 0 else 'str_grant-all-negative'
        await ctx.channel.send(
            msg_strings[send_str].format(gil_amount)
        )

        
def setup(bot):
    bot.add_cog(Administration(bot))