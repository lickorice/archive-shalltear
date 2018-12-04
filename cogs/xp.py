import discord, json, datetime, math, profiler, requests
from PIL import Image
from io import BytesIO
from discord.ext import commands
from data import db_users

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

with open("assets/obj_badges.json") as f:
    obj_badges = json.load(f)

class XPCog:
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
        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        try:
            if user_db.add_xp(message.author.id, points):
                user_db.next_level(message.author.id)
                
                # generate the image:

                profiler.level_generate(message.author.avatar_url)

                level_image = discord.File('temp/levelup.png')

                await message.channel.send(file=level_image, delete_after=10)
                
        except IndexError:
            user_db.new_user(message.author.id)
            user_db.add_xp(message.author.id, points)
        user_db.close()

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
                    await ctx.channel.send(msg_strings['str_user-not-found'])
                    return
        else:
            a = ctx.message.author

        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        equipped_badges = user_db.get_items(a.id, True)
        try:
            current_user = user_db.get_user(a.id)['users']
        except IndexError:
            await ctx.channel.send(msg_strings["str_user-not-found"])
            return
        user_db.close()

        bg_id = current_user["user_bg_id"]
        equipped_badges = list(map(lambda x: str(x["item_id"]), equipped_badges))
        level = current_user["user_level"]
        xp = (current_user["user_xp"], current_user["user_xp_to_next"])

        profiler.profile_generate(a.name, a.avatar_url, level, xp, equipped_badges, bg_id)
        profile_image = discord.File("temp/profile.png")
        await ctx.channel.send(file=profile_image)

    @commands.command()
    async def equip(self, ctx, item_id):
        """Followed by the ID, you can equip a badge."""
        if item_id not in list(obj_badges.keys()):
            await ctx.channel.send(msg_strings["str_badge-not-found"])
            return

        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        result = user_db.toggle_item(ctx.message.author.id, int(item_id))
        user_db.close()

        badge_name = obj_badges[item_id]["name"]

        if result == 1:
            await ctx.channel.send(
                msg_strings["str_badge-equipped"].format(badge_name)
                )
        elif result == 2:
            await ctx.channel.send(
                msg_strings["str_badge-unequipped"].format(badge_name)
                )
        elif result == 3:
            await ctx.channel.send(
                msg_strings["str_badge-not-yours"].format(ctx.message.author.id)
                )

    @commands.command()
    async def badges(self, ctx):
        """Shows the user's badges."""
        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect()
        badges = user_db.get_items(ctx.message.author.id)
        equipped_badges = user_db.get_items(ctx.message.author.id, True)
        user_db.close()

        badges = sorted(
            badges,
            key = lambda badge: badge["item_id"]
        )

        badge_str = ''
        
        if len(badges) == 0:
            badge_str = "You have no badges yet."
        else:
            for badge in badges:
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

        badge_str = badge_str.rstrip()

        embed = discord.Embed(
            title=ctx.message.author.display_name,
            color=0xff1155
        )
        embed.add_field(name="Your Badges", value=badge_str)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def changebg(self, ctx, bg_id):
        """Change the background of your profile."""
        with open('assets/obj_bgs.json') as f:
            bgs = list(map(int, json.load(f).keys()))
        try:
            if int(bg_id) not in bgs:
                await ctx.channel.send(msg_strings["str_bg-not-found"])
            user_db = db_users.UserHelper()
            user_db.connect()
            user_db.change_bg(ctx.message.author.id, int(bg_id))
        except ValueError:
            await ctx.channel.send(msg_strings["str_invalid-cmd"])
        user_db.close()

        
def setup(bot):
    bot.add_cog(XPCog(bot))