import discord, json, datetime, math, profiler, requests
from conf import *
from PIL import Image
from io import BytesIO
from discord.ext import commands
from data import db_users
from objects.user import User
from objects.background import Background

with open("assets/obj_badges.json") as f:
    obj_badges = json.load(f)

class Profiles:
    def __init__(self, bot):
        self.bot = bot

    # async def on_message(self, message):
    #     """Main on_message method on collecting message data."""
    #     if message.author.bot:
    #         return
    #     try:
    #         points = int(math.log(len(message.content), 2))
    #     except ValueError:
    #         points = 1
    #     user_db = db_users.UserHelper(is_logged=False)
    #     user_db.connect()
    #     try:
    #         if user_db.add_xp(message.author.id, points):
    #             user_db.next_level(message.author.id)
                
    #             # generate the image:
    #             profiler.level_generate(message.author.avatar_url)
    #             level_image = discord.File(DIR_LEVELUP)
    #             await message.channel.send(file=level_image, delete_after=10)
                
    #     except IndexError:
    #         user_db.new_user(message.author.id)
    #         user_db.add_xp(message.author.id, points)
    #     user_db.close()

    @commands.cooldown(1, 60, type=commands.BucketType.user)
    @commands.command(aliases=['p'])
    async def profile(self, ctx, target_user=None):
        """Shows the user profile of yourself, or a target user."""
        if target_user:
            try:
                a = ctx.message.mentions[0]
            except IndexError:
                a = self.bot.get_user(int(target_user))
                if not a:
                    await ctx.channel.send(MSG_USER_NOT_FOUND)
                    return
        else:
            a = ctx.author

        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        equipped_badges = user_db.get_items(a.id, True)
        try:
            current_user = user_db.get_user(a.id)['users']
        except IndexError:
            await ctx.channel.send(MSG_USER_NOT_FOUND)
            return
        user_db.close()

        bg_id = current_user["user_bg_id"]
        equipped_badges = sorted(list(map(lambda x: str(x["item_id"]), equipped_badges)))
        level = current_user["user_level"]
        xp = (current_user["user_xp"], current_user["user_xp_to_next"])

        profiler.profile_generate(a.name, a.avatar_url, level, xp, equipped_badges, bg_id)
        profile_image = discord.File(DIR_PROFILE)
        await ctx.channel.send(file=profile_image)

    @commands.command()
    async def equip(self, ctx, item_id):
        """Followed by the ID, you can equip a badge."""
        if item_id not in list(obj_badges.keys()):
            await ctx.channel.send(MSG_BADGE_NOT_FOUND)
            return

        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        equipped_badges = user_db.get_items(ctx.author.id, is_equipped=True)
        if len(equipped_badges) >= 11:
            await ctx.send(MSG_BADGE_FULL.format(ctx.author.id))
        result = user_db.toggle_item(ctx.author.id, int(item_id))
        user_db.close()

        badge_name = obj_badges[item_id]["name"]

        if result == 1:
            await ctx.channel.send(
                MSG_BADGE_EQUIPPED.format(badge_name)
                )
        elif result == 2:
            await ctx.channel.send(
                MSG_BADGE_UNEQUIPPED.format(badge_name)
                )
        elif result == 3:
            await ctx.channel.send(
                MSG_BADGE_NOT_YOURS.format(ctx.author.id)
                )

    @commands.command()
    async def badges(self, ctx):
        """Shows the user's badges."""
        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        badges = user_db.get_items(ctx.author.id)
        equipped_badges = user_db.get_items(ctx.author.id, True)
        
        # TODO: Change to Badge object.
        badges = sorted(badges, key=lambda badge: badge["item_id"])
        badge_str = ''
        
        if len(badges) == 0:
            badge_str = MSG_BADGE_NONE
        else:
            for badge in badges:
                try:
                    if badge in equipped_badges:
                        badge_str += '`ID: {}` **{}**\n'.format(
                            badge["item_id"],
                            obj_badges[str(badge["item_id"])]["name"],
                            )
                    else:
                        badge_str += '`ID: {}` {}\n'.format(
                            badge["item_id"],
                            obj_badges[str(badge["item_id"])]["name"],
                            )
                except KeyError:
                    user_db.remove_item(ctx.author.id, badge["item_id"])
        user_db.close()

        badge_str = badge_str.rstrip()

        embed = discord.Embed(
            title=ctx.author.display_name,
            color=CLR_MAIN_COLOR
        )
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