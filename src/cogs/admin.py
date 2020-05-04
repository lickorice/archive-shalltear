import discord, json, datetime
from conf import *
from discord.ext import commands
from data import db_users
from utils import msg_utils, limiters
from objects.user import User

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['k'], hidden=True)
    @limiters.is_owner()
    async def kill(self, ctx):
        """Logout command (Owner)."""
        await ctx.send(MSG_LOGGING_OUT)
        await self.bot.logout()

    @commands.command()
    @limiters.is_owner()
    async def registerall(self, ctx):
        """Adds all users (Owner)."""
        u_cnt, b_cnt = 0, 0
        
        for member in self.bot.get_all_members():
            if not member.bot:
                u = User(member.id)
                u_cnt += 1
            else:
                b_cnt += 1
        await ctx.channel.send(
            MSG_REGISTER_3.format(u_cnt + b_cnt, u_cnt, b_cnt)
        )

    @commands.command(hidden=True)
    @limiters.is_owner()
    async def resetallbgs(self, ctx):
        """Resets all backgrounds to default (Owner)."""
        for member in self.bot.get_all_members():
            if not member.bot:
                User(member.id).bg_id = 0
        await ctx.send(MSG_PROFILE_BG_RESET)

    @commands.command(aliases=['gb'], hidden=True)
    @limiters.is_owner()
    async def grantbadge(self, ctx, badge_id: int, target_user: discord.Member=None):
        """Grants a badge (Owner)."""
        print(target_user)
        if target_user == None:
            target_user = ctx.author
        
        _user = User(target_user.id)
        user_badges = _user.badges
        if badge_id in [badge.id for badge in user_badges]:
            await ctx.send(MSG_BADGE_ALREADY_EXISTS_2)
            return
        
        _user.add_badge(badge_id)
        await ctx.send(MSG_BADGE_GRANT_SUCCESS)

    @commands.command(hidden=True)
    @limiters.is_owner()
    async def grantallgil(self, ctx, gil_amount: int=0):
        """Grants all users Gil (Owner)."""
        if gil_amount == 0:
            await ctx.send(MSG_GRANT_ERROR)
            return

        for member in self.bot.get_all_members():
            if not member.bot:
                User(member.id).add_gil(gil_amount)
        send_str = MSG_GRANT_ALL_POSITIVE if gil_amount > 0 else MSG_GRANT_ALL_NEGATIVE
        await ctx.channel.send(send_str.format(gil_amount))
    
    @commands.command(hidden=True)
    @limiters.is_owner()
    async def grantgil(self, ctx, gil_amount: int=0, target_user: discord.Member=None):
        """Grants a user Gil (Owner)."""
        gil_amount = int(gil_amount)
        if gil_amount == 0:
            await ctx.send(MSG_GRANT_ERROR)
            return

        if target_user == None:
            target_user = ctx.author

        User(target_user.id).add_gil(gil_amount)
        send_str = MSG_GRANT_POSITIVE if int(gil_amount) > 0 else MSG_GRANT_NEGATIVE
        await ctx.channel.send(send_str.format(target_user.id, gil_amount))
    
    @commands.command(hidden=True)
    @limiters.is_owner()
    async def setpremium(self, ctx, target_user: discord.Member=None):
        """Sets a user's premium status (Owner)."""
        if target_user == None:
            target_user = ctx.author

        _u = User(target_user.id)
        _x = _u.toggle_premium()
        string = MSG_SET_PREMIUM1 if _x else MSG_SET_PREMIUM2
        await ctx.send(string.format(ctx.author.display_name))

def setup(bot):
    bot.add_cog(Administration(bot))