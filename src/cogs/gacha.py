import discord, json, datetime, random
from conf import *
from discord.ext import commands
from data import db_gacha
from errors import *
from objects.booster_pack import BoosterPack
from objects.card import Card
from objects.series import Series
from objects.user import User
from utils import msg_utils, limiters

streak_counter = {}
# user_id : streak_count
rarity_config = {
    1:  (30, 7, 3, 2, 1, 0),
    3:  (0, 30, 7, 3, 2, 0),
    5:  (0, 0, 30, 7, 3, 0),
    7:  (0, 0, 0, 10, 3, 0),
    10: (0, 0, 0, 0, 3, 1)
}

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

stored_messages = {}
stored_packs = {}

def get_card(arg):
    try:
        arg = int(arg) # This means user put in an ID
        return Card.get_from_id(arg)
    except ValueError:
        return Card.get_from_name(arg)

def get_series(arg):
    try:
        arg = int(arg) # This means user put in an ID
        return Series.get_from_id(arg)
    except ValueError:
        return Series.get_from_name(arg)

class Gacha(commands.Cog):

    async def detect_turn(self, reaction, user):
        target_id = reaction.message.id
        if user.id in stored_messages:
            if target_id == stored_messages[user.id][0]:
                p, series = stored_messages[user.id][1], stored_messages[user.id][3]
                if reaction.emoji == EMJ_LEFT_PAGE:
                    p = (p-1)%series.max_pages
                    e = series.make_embed(p)
                    await reaction.message.edit(embed=e)
                elif reaction.emoji == EMJ_RIGHT_PAGE:
                    p = (p+1)%series.max_pages
                    e = series.make_embed(p)
                    await reaction.message.edit(embed=e)
                stored_messages[user.id] = (target_id, p, reaction.message, series)
        elif user.id in stored_packs:
            if target_id == stored_packs[user.id][0]:
                bpack = stored_packs[user.id][1]
                if reaction.emoji == EMJ_LEFT_PAGE:
                    stored_packs[user.id][1].page = (stored_packs[user.id][1].page-1) % stored_packs[user.id][1].card_count
                    e = stored_packs[user.id][1].make_embed()
                    await reaction.message.edit(embed=e)
                elif reaction.emoji == EMJ_RIGHT_PAGE:
                    stored_packs[user.id][1].page = (stored_packs[user.id][1].page+1) % stored_packs[user.id][1].card_count 
                    e = stored_packs[user.id][1].make_embed()
                    await reaction.message.edit(embed=e)

    async def on_reaction_add(self, reaction, user):
        await self.detect_turn(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        await self.detect_turn(reaction, user)

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['m', 'mbal', 'mbalance', 'm$'])
    async def materia(self, ctx, target_user: discord.Member=None):
        """Check your own materia, or another user's materia."""
        if target_user == None:
            target_user = ctx.author

        string = MSG_MATERIA_CHECK if target_user == None else MSG_MATERIA_CHECK2
        await ctx.channel.send(string.format(
            target_user.display_name, User(target_user.id).materia))

    @commands.command(aliases=['ccards'], hidden=True)
    @limiters.is_owner()
    async def consolidatecards(self, ctx):
        """Manually consolidates the cards from the Google Sheets spreadsheets (Owner)."""
        db = db_gacha.GachaHelper(False)
        db.connect()
        result1 = db.consolidate_cards()
        result2 = db.consolidate_series()
        db.close()
        await ctx.send(f"Successfully consolidated all **{result1}** cards and **{result2}** series.")
        
    @commands.command(aliases=['bcards'], hidden=True)
    @limiters.is_owner()
    async def backupcards(self, ctx):
        """Manually backup the card database to Google Sheets."""
        pass

    @commands.command(aliases=['vc'])
    async def viewcard(self, ctx, *card):
        """Views a card given its information."""
        try:
            card = get_card(' '.join(card))
        except CardNotFound:
            await ctx.send(MSG_GACHA_CARD_DNE.format(ctx.author.display_name))
            return
        e = card.make_embed()
        await ctx.send(embed=e)
        # TODO: Pagify, add enchant/craft info on other page
        
    @commands.command(aliases=['vs'])
    async def viewseries(self, ctx, *series):
        """Views a series given its information."""
        try:
            series = get_series(' '.join(series))
        except SeriesNotFound:
            await ctx.send(MSG_GACHA_SERIES_DNE.format(ctx.author.display_name))
            return
        e = series.make_embed()
        msg = await ctx.send(embed=e)
        if series.max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)
            stored_messages[ctx.author.id] = (msg.id, 0, msg, series)

    @commands.command(aliases=['ci'])
    @commands.cooldown(1, 30, type=commands.BucketType.user)
    async def cardinventory(self, ctx):
        """View your card inventory."""

    @commands.command(aliases=['fc'])
    async def freecards(self, ctx):
        """Claim free cards every 1 hour, takes note of streaks!"""
        # Free card rates:
        #     1*-5* for 1 streaks
        #     2*-5* for 3 streaks
        #     3*-5* for 5 streaks
        #     4*-5* for 7 streaks
        #     5*-6* for 10 streaks
        #     resets after 12 streaks
        
        current_streak = 1
        if ctx.author.id in streak_counter:
            current_streak = streak_counter[ctx.author.id]
            if current_streak == 13:
                streak_counter[ctx.author.id] = 1
                current_streak = 1 # reset the streak
        else:
            streak_counter[ctx.author.id] = 1

        current_config = ()
        while True:
            if current_streak in rarity_config:
                current_config = rarity_config[current_streak]
                break
            else:
                current_streak -= 1

        rating_list = []
        for i in range(6):
            rating_list += [i+1 for _i in range(current_config[i])]
        random.shuffle(rating_list)

        card_list = Card.make_booster_pack(rating_list[0:3])
        _u = User(ctx.author.id)
        for card in card_list:
            if not card.acquired:
                card.register_first(ctx.author)
            _u.gacha.add_card(card)
            
        booster_pack = BoosterPack(card_list, ctx.author)

        e = booster_pack.make_embed()

        a, b = ctx.author.display_name, streak_counter[ctx.author.id]
        streak_counter[ctx.author.id] += 1

        msg = await ctx.send(MSG_GACHA_STREAK.format(a, b), embed=e)
        stored_packs[ctx.author.id] = (msg.id, booster_pack)
        await msg.add_reaction(EMJ_LEFT_PAGE)
        await msg.add_reaction(EMJ_RIGHT_PAGE)

    @commands.command(aliases=['sc'])
    async def summoncards(self):
        """Use up materia to summon cards."""
        pass

    @commands.command()
    async def craftcard(self, ctx, *card):
        """Craft a card using its corresponding ingredients."""
        pass

    @commands.command()
    async def banishcard(self, ctx, *card):
        """Banish a card and gain materia."""
        pass

    @commands.command(aliases=['ec'])
    async def enchant(self, ctx, *card):
        """Enchant a card using materia and duplicates."""
        pass
    
def setup(bot):
    bot.add_cog(Gacha(bot))