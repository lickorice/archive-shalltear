import discord, json, datetime
from conf import *
from discord.ext import commands
from data import db_gacha
from errors import *
from objects.card import Card
from objects.series import Series
from objects.user import User
from utils import msg_utils, limiters

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

stored_messages = {}

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

class Gacha:
    async def on_reaction_add(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
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

    async def on_reaction_remove(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
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

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ccards'], hidden=True)
    @limiters.is_owner()
    async def consolidatecards(self, ctx):
        """Consolidates the cards from the Google Sheets spreadsheets (Owner)."""
        db = db_gacha.GachaHelper(False)
        db.connect()
        result1 = db.consolidate_cards()
        result2 = db.consolidate_series()
        db.close()
        await ctx.send(f"Successfully consolidated all **{result1}** cards and **{result2}** series..")
        
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
        e = series.make_embed(0)
        msg = await ctx.send(embed=e)
        if series.max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)
            stored_messages[ctx.author.id] = (msg.id, 0, msg, series)

    @commands.command(aliases=['fc'])
    async def freecards(self, ctx):
        """Claim free cards every 1 hour, takes note of streaks!"""
        pass

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
    async def enchant(self, ctx, *card)
        """Enchant a card using materia and duplicates."""
        pass
    
def setup(bot):
    bot.add_cog(Gacha(bot))