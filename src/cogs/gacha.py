import discord, json, datetime
from conf import *
from discord.ext import commands
from data import db_gacha
from errors import *
from objects.user import User
from objects.card import Card
from utils import msg_utils, limiters

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

def get_card(arg):
    try:
        arg = int(arg) # This means user put in an ID
        return Card.get_from_id(arg)
    except ValueError:
        return Card.get_from_name(arg)

class Administration:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ccards'], hidden=True)
    @limiters.is_owner()
    async def consolidatecards(self, ctx):
        """Consolidates the cards from the Google Sheets spreadsheets (Owner)."""
        db = db_gacha.GachaHelper(False)
        db.connect()
        result = db.consolidate_cards()
        db.close()
        await ctx.send(f"Successfully consolidated all **{result}** cards.")
        
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
    
def setup(bot):
    bot.add_cog(Administration(bot))