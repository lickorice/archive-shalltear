import discord, json, datetime, time, math
from conf import *
from discord.ext import commands
from data import db_users
from utils import msg_utils
from objects.user import User
from objects.badge import Badge
from objects.background import Background

stored_messages = {}

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

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
            return Badge(target_id)
        elif json_name == "bgs":
            return Background(target_id)

class Shop:
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

    @commands.command()
    async def badgebuy(self, ctx, *target_item):
        """This will buy a badge given its ID or its name (exact)."""
        target_item = ' '.join(target_item)
        item = get_target_item(target_item, "badgeshop")
        if item == None:
            await ctx.send(MSG_BADGE_NOT_FOUND)
            return

        _user = User(ctx.author.id)

        if item.id in [item.id for item in _user.badges]:
            await ctx.send(MSG_BADGE_ALREADY_YOURS.format(ctx.author.id))
            return
        if _user.gil < item.price:
            await ctx.send(MSG_INSUF_GIL)
            return
        if _user.level < item.level_needed:
            await ctx.send(MSG_INSUF_LVL)
            return
        if not item.is_for_sale:
            await ctx.send(MSG_ITEM_NOT_FOR_SALE)
            return
        if item.is_exclusive and (ctx.guild.id != OWNER_GUILD_ID):
            await ctx.send(MSG_ITEM_IS_EXCLUSIVE)
            return
        
        _user.add_gil(-item.price)
        _user.add_badge(item.id)

        await ctx.send(MSG_BADGE_BOUGHT.format(ctx.author.id, item.name))

        # special badges here:
        if item.id == 0: # VIP badge
            await ctx.author.add_roles(ctx.guild.get_role(VIP_ROLE_ID))
            vip_channel = self.bot.get_channel(VIP_CHANNEL_ID)
            await vip_channel.send(MSG_VIP_WELCOME.format(ctx.author.id))
        elif item.id == 7:
            role_name = None
            _x = ctx.author.id
            while True:
                def check(m):
                    return len(m.content) <= 32 and m.author.id == ctx.author.id

                await ctx.send(MSG_NEET_ROLE_NAME_WAIT.format(_x))
                role_name = await self.bot.wait_for('message', check=check)
                role_name = role_name.content

                def check2(m):
                    return (m.content.lower() == 'y' or m.content.lower() == 'n') and m.author.id == ctx.author.id
        
                await ctx.send(MSG_NEET_ROLE_CONFIRM.format(_x, role_name))
                confirmation = await self.bot.wait_for('message', check=check2)
                confirmation = confirmation.content
                if confirmation == 'y':
                    break
            
            new_role = await ctx.guild.create_role(name=role_name, color=discord.Color(0xff1155))
            await ctx.send(MSG_NEET_ROLE_CREATE.format(_x, role_name))
            await ctx.author.add_roles(new_role)

    @commands.command()
    async def bgbuy(self, ctx, *target_item):
        """This will buy a profile background given its ID or its name (exact)."""
        target_item = ' '.join(target_item)
        item = get_target_item(target_item, "bgs")
        if item == None:
            await ctx.send(MSG_BG_NOT_FOUND)
            return
        
        _user = User(ctx.author.id)

        if item.id in [bg.id for bg in _user.backgrounds]:
            await ctx.send(MSG_BG_ALREADY_YOURS.format(ctx.author.id))
            return
        if _user.gil < item.price:
            await ctx.send(MSG_INSUF_GIL)
            return
        if not item.is_for_sale:
            await ctx.send(MSG_ITEM_NOT_FOR_SALE)
            return
        if item.is_exclusive and (ctx.guild.id != OWNER_GUILD_ID):
            await ctx.send(MSG_ITEM_IS_EXCLUSIVE)
            return
        
        _user.add_gil(-item.price)
        _user.add_bg(item.id)

        await ctx.send(MSG_BG_BOUGHT.format(ctx.author.id, item.name, item.price))

    @commands.command()
    async def badgeshop(self, ctx):
        """Shows the shop screen for badges."""
        a = ctx.message.author
        with open('assets/obj_badgeshop.json') as f:
            badge_shop = json.load(f)
        item_list = []
        for item_id in badge_shop:
            item_list.append(Badge(item_id))

        _user = User(ctx.author.id)

        # generate the embed
        max_pages = math.ceil(len(item_list) / 5)
        p = msg_utils.PaginatedEmbed(_user.badges, item_list, 0, "badgeshop", max_pages)
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)
        
        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)

    @commands.command()
    async def bgshop(self, ctx):
        """Shows the shop screen for profile backgrounds."""
        a = ctx.message.author
        with open('assets/obj_bgs.json') as f:
            bg_shop = json.load(f)
        item_list = []
        for item_id in bg_shop:
            item_list.append(Background(item_id))
                
        _user = User(ctx.author.id)

        # generate the embed
        item_list = sorted(item_list, key=lambda x: x.name)
        max_pages = math.ceil(len(item_list) / 5)
        p = msg_utils.PaginatedEmbed(_user.backgrounds, item_list, 0, "bgshop", max_pages)
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)

        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)

def setup(bot):
    bot.add_cog(Shop(bot))