import discord, json, datetime
from conf import *
from discord.ext import commands
from data import db_users
from utils import msg_utils, limiters
from objects.user import User

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Administration:

    # TODO: Build up a plant library with name, price
    # TODO: View inventory of a player
    # TODO: Develop a game engine that cycles every 30 seconds

    async def cycle(self):
        """Increment time for planting."""
        pass

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['gts'])
    async def giltoshekels(self, ctx):
        """Convert gil to shekels by 1:10."""
        pass

    @commands.command(aliases=['gts'])
    async def shekelstogil(self, ctx):
        """Convert shekels to gil by 100:1."""
        pass

    @commands.command()
    async def plantshop(self, ctx):
        """See the catalog for plants."""
        pass

    @commands.command()
    async def buyplant(self, ctx, count, *plant_name):
        """Purchase plant seeds."""
        pass

    @commands.command()
    async def plant(self, ctx, count, *plant_name):
        """Plant the seeds of a plant to be harvested later."""
        pass

    @commands.command(aliases=['stinfo'])
    async def harvest(self, ctx, plot_number):
        """Harvest a certain plot with harvestable plants."""
        pass

    @commands.command()
    async def plantall(self, ctx, count, *plant_name):
        """Plant the seeds of a plant on all available plots."""
        pass

    @commands.command(aliases=['stinfo'])
    async def harvestall(self, ctx):
        """Harvest all the harvestable plots you can see."""
        pass

    @commands.command()
    async def construct(self, ctx, *structure_name):
        """Construct a structure to upgrade your production!"""
        pass

    @commands.command()
    async def plotinfo(self, ctx, *structure_name):
        """See information on a certain plot."""
        pass

        
def setup(bot):
    bot.add_cog(Administration(bot))