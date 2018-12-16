import discord, json, datetime, math, profiler, requests
from conf import *
from PIL import Image
from io import BytesIO
from discord.ext import commands
from data import db_users
from objects.user import User
from objects.background import Background
from objects.badge import Badge
from utils import msg_utils

with open("assets/obj_badges.json") as f:
    obj_badges = json.load(f)

class Profiles:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        """Main on_message method on collecting message data."""
        if message.author.bot:
            return
        try:
            points = int(math.log(len(message.content), 2))
        except ValueError:
            points = 1
        if User(message.author.id).add_xp(points):
            # generate the image:
            profiler.level_generate(message.author.avatar_url)
            level_image = discord.File(DIR_LEVELUP)
            await message.channel.send(file=level_image, delete_after=10)

    @commands.cooldown(1, 60, type=commands.BucketType.user)
    @commands.command(aliases=['p'])
    async def profile(self, ctx, target_user=None):
        """Shows the user profile of yourself, or a target user."""
        a = await msg_utils.get_target_user(ctx, target_user)

        if a == None:
            await ctx.send(MSG_USER_NOT_FOUND)
            return

        _u = User(a.id)
        equipped_badges = [badge for badge in _u.badges if badge.is_equipped]

        profiler.profile_generate(a.name, a.avatar_url, _u.level, (_u.xp, _u.xp_to_next), equipped_badges, _u.bg_id)
        profile_image = discord.File(DIR_PROFILE)
        await ctx.channel.send(file=profile_image)

    @commands.command()
    async def equip(self, ctx, badge_id):
        """Followed by the ID, you can equip a badge."""
        if badge_id not in list(obj_badges.keys()):
            await ctx.channel.send(MSG_BADGE_NOT_FOUND)
            return

        try:
            current_badge = Badge(int(badge_id))
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)
            return

        _user = User(ctx.author.id)
        equipped_badges = [badge for badge in _user.badges if badge.is_equipped]
        if len(equipped_badges) >= 11:
            await ctx.send(MSG_BADGE_FULL.format(ctx.author.id))
            return

        result = _user.equip_badge(current_badge.id)

        if result == 1:
            await ctx.channel.send(
                MSG_BADGE_EQUIPPED.format(current_badge.name)
                )
        elif result == 2:
            await ctx.channel.send(
                MSG_BADGE_UNEQUIPPED.format(current_badge.name)
                )
        elif result == 3:
            await ctx.channel.send(
                MSG_BADGE_NOT_YOURS.format(ctx.author.id)
                )

    @commands.command()
    async def badges(self, ctx):
        """Shows the user's badges."""
        _user = User(ctx.author.id)
        
        if len(_user.badges) == 0:
            badge_str = MSG_BADGE_NONE
        else:
            badge_str = ''
            for badge in _user.badges:
                try:
                    if badge.is_equipped:
                        badge_str += '`ID: {}` **{}**\n'.format(
                            badge.id, badge.name)
                    else:
                        badge_str += '`ID: {}` {}\n'.format(
                            badge.id, badge.name)
                except KeyError:
                    _user.remove_badge()

        badge_str = badge_str.rstrip()

        embed = discord.Embed(
            title=ctx.author.display_name,
            color=CLR_MAIN_COLOR
        )

        # TODO: Paginate

        embed.add_field(name="Your Badges", value=badge_str)
        await ctx.channel.send(embed=embed)
        
    @commands.command()
    async def changebg(self, ctx, bg_id):
        """Changes the background of your profile."""
        _user = User(ctx.author.id)
        try:
            if int(bg_id) in [bg.id for bg in _user.backgrounds]:
                _user.bg_id = bg_id
                await ctx.send(
                    MSG_BG_CHANGED.format(
                        ctx.author.display_name, Background(bg_id).name
                        )
                )
            else:
                await ctx.send(MSG_BG_NOT_YOURS.format(ctx.author.name))
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)

    @commands.cooldown(1, 60, type=commands.BucketType.user)
    @commands.command()
    async def previewbg(self, ctx, bg_id):
        """Previews a background given its ID."""
        try:
            bg_id = int(bg_id)
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)
            return
        
        with open('assets/obj_bgs.json') as f:
            all_bgs = json.load(f)
        
        if str(bg_id) not in all_bgs:
            await ctx.send(MSG_BG_NOT_FOUND)
        profiler.profile_generate(ctx.author.name, ctx.author.avatar_url, 20, (1, 2), [], int(bg_id))
        profile_image = discord.File(DIR_PROFILE)
        await ctx.channel.send(MSG_BG_PREVIEW.format(all_bgs[str(bg_id)]["name"]))
        await ctx.channel.send(file=profile_image)

def setup(bot):
    bot.add_cog(Profiles(bot))