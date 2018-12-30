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

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

with open("assets/obj_badges.json") as f:
    obj_badges = json.load(f)

stored_messages = {}

class Profiles:
    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == EMJ_LEFT_PAGE:
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == EMJ_RIGHT_PAGE:
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    async def on_reaction_remove(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == EMJ_LEFT_PAGE:
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == EMJ_RIGHT_PAGE:
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    async def on_message(self, message):
        """Main on_message method on collecting message data."""
        if message.guild is None:
            return
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
            try:
                await message.channel.send(file=level_image, delete_after=10)
            except discord.errors.Forbidden:
                log(f"[ERR] Forbidden to send a message in this channel: {msg.channel.name} @ {msg.guild.name}")

    @commands.cooldown(1, 60, type=commands.BucketType.user)
    @commands.command(aliases=['p'])
    @commands.guild_only()
    async def profile(self, ctx, target_user: discord.Member=None):
        """Shows the user profile of yourself, or a target user."""
        if target_user == None:
            target_user = ctx.author

        _u = User(target_user.id)
        equipped_badges = [badge for badge in _u.badges if badge.is_equipped]

        profiler.profile_generate(
            target_user.name, target_user.avatar_url,
            _u.level, (_u.xp, _u.xp_to_next), equipped_badges, _u.bg_id, _u.is_premium
            )
        profile_image = discord.File(DIR_PROFILE)
        await ctx.channel.send(file=profile_image)

    @commands.command()
    @commands.guild_only()
    async def equip(self, ctx, badge_id: int):
        """Followed by the ID, you can equip a badge."""
        if str(badge_id) not in list(obj_badges.keys()):
            await ctx.channel.send(MSG_BADGE_NOT_FOUND)
            return

        current_badge = Badge(badge_id)

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
    @commands.guild_only()
    async def badges(self, ctx):
        """Shows the user's badges."""
        _user = User(ctx.author.id)
        
        if len(_user.badges) == 0:
            await ctx.send(MSG_BADGE_NONE.format(ctx.author.display_name))
            return
            
        # generate the embed
        max_pages = math.ceil(len(_user.badges) / 10)
        p = msg_utils.PaginatedEmbed(
            [], _user.badges, 0, "badges",
            max_pages, name=ctx.author.display_name
        )
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)
        
        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)
        
    @commands.command()
    @commands.guild_only()
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
    @commands.guild_only()
    async def previewbg(self, ctx, bg_id: int):
        """Previews a background given its ID."""
        with open('assets/obj_bgs.json') as f:
            all_bgs = json.load(f)
        
        if str(bg_id) not in all_bgs:
            await ctx.send(MSG_BG_NOT_FOUND)

        _u = User(ctx.author.id)
        profiler.profile_generate(ctx.author.name, ctx.author.avatar_url, 20, (1, 2), [], bg_id, _u.is_premium)
        profile_image = discord.File(DIR_PROFILE)
        await ctx.channel.send(MSG_BG_PREVIEW.format(all_bgs[str(bg_id)]["name"]))
        await ctx.channel.send(file=profile_image)

def setup(bot):
    bot.add_cog(Profiles(bot))