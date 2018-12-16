import discord, json, datetime
from conf import *
from discord.ext import commands
from data import db_users
from utils import msg_utils
from objects.user import User

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
        if ctx.author.id == OWNER_ID:
            await ctx.send(MSG_LOGGING_OUT)
            await self.bot.logout()
        else:
            await ctx.channel.send(MSG_INSUF_PERMS)

    @commands.command()
    async def registerall(self, ctx):
        """Adds all users (Owner)."""
        if ctx.author.id != OWNER_ID:
            await ctx.channel.send(MSG_INSUF_PERMS)
            return

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

    @commands.command()
    async def resetallbgs(self, ctx):
        """Resets all backgrounds to default (Owner)."""
        if ctx.author.id != OWNER_ID:
            await ctx.channel.send(MSG_INSUF_PERMS)
            return
        for member in self.bot.get_all_members():
            if not member.bot:
                User(member.id).bg_id = 0
        await ctx.send(MSG_PROFILE_BG_RESET)

    @commands.command(aliases=['gb'])
    async def grantbadge(self, ctx, badge_id, target_user=None):
        """Grants a badge (Owner)."""
        if ctx.message.author.id != OWNER_ID:
            await ctx.send(MSG_INSUF_PERMS)
            return
        try:
            badge_id = int(badge_id)
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)
            return
        
        a = await msg_utils.get_target_user(ctx, target_user)
        if a == None:
            await ctx.send(MSG_USER_NOT_FOUND)
            return
        
        _user = User(a.id)
        user_badges = _user.badges
        if badge_id in [badge.id for badge in user_badges]:
            await ctx.send(MSG_BADGE_ALREADY_EXISTS_2)
            return
        
        _user.add_badge(badge_id)
        await ctx.send(MSG_BADGE_GRANT_SUCCESS)

    @commands.command()
    async def grantallgil(self, ctx, gil_amount=0):
        """Grants all users Gil (Owner)."""
        if ctx.message.author.id != OWNER_ID:
            await ctx.send(MSG_INSUF_PERMS)
            return

        try:
            gil_amount = int(gil_amount)
            if gil_amount == 0:
                await ctx.send(MSG_GRANT_ERROR)
                return
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)

        for member in self.bot.get_all_members():
            if not member.bot:
                User(member.id).add_gil(gil_amount)
        send_str = MSG_GRANT_ALL_POSITIVE if gil_amount > 0 else MSG_GRANT_ALL_NEGATIVE
        await ctx.channel.send(send_str.format(gil_amount))
    
    @commands.command()
    async def grantgil(self, ctx, gil_amount=0, target_user=None):
        """Grants a user Gil (Owner)."""
        if ctx.message.author.id != OWNER_ID:
            await ctx.send(MSG_INSUF_PERMS)
            return
        
        try:
            gil_amount = int(gil_amount)
            if gil_amount == 0:
                await ctx.send(MSG_GRANT_ERROR)
                return
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)

        a = await msg_utils.get_target_user(ctx, target_user)

        if a == None:
            await ctx.send(MSG_USER_NOT_FOUND)
            return

        User(a.id).add_gil(gil_amount)
        send_str = MSG_GRANT_POSITIVE if int(gil_amount) > 0 else MSG_GRANT_NEGATIVE
        await ctx.channel.send(send_str.format(a.id, gil_amount))

        
def setup(bot):
    bot.add_cog(Administration(bot))