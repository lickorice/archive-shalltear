import discord, json, datetime, conf
from discord.ext import commands
from data import db_users
from utils import msg_utils

config = conf.Config()

# TODO: Test all commands to check if config migration is a success.

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
            await ctx.send(config.MSG_LOGGING_OUT)
            await self.bot.logout()
        else:
            await ctx.channel.send(config.MSG_INSUF_PERMS)

    @commands.command()
    async def registerall(self, ctx):
        """Adds all users (Owner)."""
        if ctx.author.id != config.OWNER_ID:
            await ctx.channel.send(config.MSG_INSUF_PERMS)
            return
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
            config.MSG_REGISTER_3.format(all_count, reg_count, bot_count)
            )

    @commands.command()
    async def resetallbgs(self, ctx):
        """Resets all backgrounds to default (Owner)."""
        if ctx.author.id != config.OWNER_ID:
            await ctx.channel.send(config.MSG_INSUF_PERMS)
            return
        user_db = db_users.UserHelper()
        user_db.connect()
        for member in self.bot.get_all_members():
            if not member.bot:
                user_db.change_bg(member.id, 0)
        user_db.close()

    @commands.command(aliases=['gb'])
    async def grantbadge(self, ctx, item_id=None, target_user=None):
        # TODO: Test this command, dawg.
        """Grants a badge (Owner)."""
        if ctx.message.author.id != config.OWNER_ID:
            await ctx.send(config.MSG_INSUF_PERMS)
            return
        if item_id == None:
            await ctx.send(config.MSG_INVALID_CMD)
            return
        try:
            # TODO: Make a utility function to check integrity of args :((((
            item_id = int(item_id)
        except ValueError:
            await ctx.send(config.MSG_INVALID_CMD)
            return
        
        a = await msg_utils.get_target_user(ctx, target_user)

        if a == None:
            await ctx.send(config.MSG_USER_NOT_FOUND)
            return

        user_db = db_users.UserHelper()
        user_db.connect()
        
        user_items = user_db.get_items(a.id)
        # TODO: Make UserHelper.get_items return badge-specific objects
        # TODO: Make all "items" to "badges" to be more appropriate
        user_items = [item["item_id"] for item in user_items]
        
        if item_id in user_items:
            await ctx.send(config.MSG_BADGE_ALREADY_EXISTS_2)
            user_db.close()
            return

        user_db.add_item(a.id, item_id)
        user_db.close()

        await ctx.send(config.MSG_BADGE_GRANT_SUCCESS)

    @commands.command()
    async def grantallgil(self, ctx, gil_amount=0):
        """Grants all users Gil (Owner)."""
        if ctx.message.author.id != config.OWNER_ID:
            await ctx.send(config.MSG_INSUF_PERMS)
            return

        try:
            gil_amount = int(gil_amount)
            if gil_amount == 0:
                await ctx.send(config.MSG_GRANT_ERROR)
                return
        except ValueError:
            await ctx.send(config.MSG_INVALID_CMD)

        user_db = db_users.UserHelper()
        user_db.connect()
        for member in self.bot.get_all_members():
            if not member.bot:
                user_db.add_gil(member.id, gil_amount)
        user_db.close()
        send_str = config.MSG_GRANT_ALL_POSITIVE if gil_amount > 0 else config.MSG_GRANT_ALL_NEGATIVE
        await ctx.channel.send(send_str.format(gil_amount))
    
    @commands.command()
    async def grantgil(self, ctx, gil_amount=0, target_user=None):
        """Grants a user Gil (Owner)."""
        if ctx.message.author.id != config.OWNER_ID:
            await ctx.send(config.MSG_INSUF_PERMS)
            return
        
        try:
            gil_amount = int(gil_amount)
            if gil_amount == 0:
                await ctx.send(config.MSG_GRANT_ERROR)
                return
        except ValueError:
            await ctx.send(config.MSG_INVALID_CMD)

        a = await msg_utils.get_target_user(ctx, target_user)

        if a == None:
            await ctx.send(config.MSG_USER_NOT_FOUND)
            return

        user_db = db_users.UserHelper()
        user_db.connect()
        user_db.add_gil(a.id, gil_amount)
        user_db.close()
        send_str = config.MSG_GRANT_POSITIVE if int(gil_amount) > 0 else config.MSG_GRANT_NEGATIVE
        await ctx.channel.send(send_str.format(a.id, gil_amount))

        
def setup(bot):
    bot.add_cog(Administration(bot))