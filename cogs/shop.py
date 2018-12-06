import discord, json, datetime, time, conf, math
from discord.ext import commands
from data import db_users
from utils import msg_utils

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

config = conf.Config()
stored_messages = {}

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class BadgeItem:
    """
    Instantiates a Badge object given an ID, and given that
    it exists in the JSON file.
    
    Args:
        item_id (int): The ID of the badge.
    """
    def __init__(self, item_id):
        with open('assets/obj_badgeshop.json') as f:
            badge_shop = json.load(f)
        self.id = int(item_id)
        item_id = str(item_id)
        self.name = badge_shop[item_id]["name"]
        self.is_exclusive = badge_shop[item_id]["is_exclusive"]
        self.price = badge_shop[item_id]["price"]
        self.price_tag = badge_shop[item_id]["price_tag"]
        self.level_needed = badge_shop[item_id]["level_needed"]
        self.icon_url = badge_shop[item_id]["icon_url"]
        self.description = badge_shop[item_id]["description"]


class BGItem:
    """
    Instantiates a Background object given an ID, and given that
    it exists in the JSON file.
    
    Args:
        bg_id (int): The ID of the background.
    """
    def __init__(self, bg_id):
        with open('assets/obj_bgs.json') as f:
            bg_shop = json.load(f)
        self.id = int(bg_id)
        bg_id = str(bg_id)
        self.img_url = bg_shop[bg_id]["img_url"]
        self.is_exclusive = bg_shop[bg_id]["is_exclusive"]
        self.price = bg_shop[bg_id]["price"]
        self.price_tag = bg_shop[bg_id]["price_tag"]
        self.name = bg_shop[bg_id]["name"]


def get_target_item(target_item, json_name):
    with open('assets/obj_{}.json'.format(json_name)) as f:
        badge_shop = json.load(f)

    try:
        target_id = int(target_item)
    except ValueError:
        target_id = None
        for item_id in badge_shop:
            if badge_shop[item_id]["name"].lower() == target_item.lower():
                target_id = item_id
                break
    if target_id == None or str(target_id) not in badge_shop:
        return None
    else:
        if json_name == "badgeshop":
            return BadgeItem(target_id)
        elif json_name == "bgs":
            return BGItem(target_id)


class Shop:
    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == '◀':
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == '▶':
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    async def on_reaction_remove(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == '◀':
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == '▶':
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    @commands.command()
    async def badgebuy(self, ctx, *target_item):
        """This will buy a badge given its ID or its name (exact)."""
        target_item = ' '.join(target_item)
        item = get_target_item(target_item, "badgeshop")
        if item == None:
            await ctx.send(msg_strings["str_badge-not-found"])
            return
        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect() # TODO: deprecate this please
        user_info = user_db.get_user(ctx.author.id)["users"]
        current_gil, current_level = user_info["user_gil"], user_info["user_level"]
        current_items = [item["item_id"] for item in user_db.get_items(ctx.author.id)]
        if item.id in current_items:
            await ctx.send(msg_strings["str_badge-already-yours"].format(ctx.author.id))
            user_db.close()
            return
        if current_gil < item.price:
            await ctx.send(msg_strings["str_insuf-gil"])
            user_db.close()
            return
        if current_level < item.level_needed:
            await ctx.send(msg_strings["str_insuf-lvl"])
            user_db.close()
            return
        
        user_db.add_gil(ctx.author.id, -item.price)
        user_db.add_item(ctx.author.id, item.id)

        await ctx.send(msg_strings["str_badge-bought"].format(ctx.author.id, item.name))

        # special badges here:
        if item.id == 0: # VIP badge
            await ctx.author.add_roles(ctx.guild.get_role(config.VIP_ROLE_ID))
            vip_channel = self.bot.get_channel(config.VIP_CHANNEL_ID)
            await vip_channel.send(msg_strings["str_vip-welcome"].format(ctx.author.id))
        user_db.close()

    @commands.command()
    async def bgbuy(self, ctx, *target_item):
        """This will buy a profile background given its ID or its name (exact)."""
        target_item = ' '.join(target_item)
        item = get_target_item(target_item, "bgs")
        if item == None:
            await ctx.send(msg_strings["str_bg-not-found"])
            return
        
        user_db = db_users.UserHelper(is_logged=False)
        user_db.connect() # TODO: deprecate this please
        user_info = user_db.get_user(ctx.author.id)["users"]
        
        current_gil, current_level = user_info["user_gil"], user_info["user_level"]
        current_items = [item["bg_id"] for item in user_db.get_backgrounds(ctx.author.id)]
        
        if item.id in current_items:
            await ctx.send(msg_strings["str_bg-already-yours"].format(ctx.author.id))
            user_db.close()
            return
        if current_gil < item.price:
            await ctx.send(msg_strings["str_insuf-gil"])
            user_db.close()
            return
        
        user_db.add_gil(ctx.author.id, -item.price)
        user_db.add_bg(ctx.author.id, item.id)

        await ctx.send(msg_strings["str_bg-bought"].format(ctx.author.id, item.name, item.price))

        user_db.close()

    @commands.command()
    async def badgeshop(self, ctx):
        """Shows the shop screen for badges."""
        a = ctx.message.author
        with open('assets/obj_badgeshop.json') as f:
            badge_shop = json.load(f)
        item_list = []
        for item_id in badge_shop:
            item = BadgeItem(item_id)
            # filters out the exclusive IPM-only stuff
            if (item.is_exclusive and ctx.guild.id == config.OWNER_GUILD_ID) or not item.is_exclusive:
                item_list.append(item)

        user_db = db_users.UserHelper()
        user_db.connect() # TODO: outstanding connect
        owned_list = [item["item_id"] for item in user_db.get_items(ctx.author.id)]
        user_db.close()

        # generate the embed
        max_pages = math.ceil(len(item_list) / 5)
        p = msg_utils.PaginatedEmbed(owned_list, item_list, 0, "badgeshop", max_pages)
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)
        
        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction('◀')
            await msg.add_reaction('▶')

    @commands.command()
    async def bgshop(self, ctx):
        """Shows the shop screen for profile backgrounds."""
        a = ctx.message.author
        with open('assets/obj_bgs.json') as f:
            bg_shop = json.load(f)
        item_list = []
        for item_id in bg_shop:
            item = BGItem(item_id)
            # filters out the exclusive IPM-only stuff
            if (item.is_exclusive and ctx.guild.id == config.OWNER_GUILD_ID) or not item.is_exclusive:
                item_list.append(item)
                
        user_db = db_users.UserHelper()
        user_db.connect() # TODO: outstanding connect
        owned_list = [item["bg_id"] for item in user_db.get_backgrounds(ctx.author.id)]
        user_db.close()

        # generate the embed
        item_list = sorted(item_list, key=lambda x: x.name)
        max_pages = math.ceil(len(item_list) / 5)
        p = msg_utils.PaginatedEmbed(owned_list, item_list, 0, "bgshop", max_pages)
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)

        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction('◀')
            await msg.add_reaction('▶')

        
def setup(bot):
    bot.add_cog(Shop(bot))