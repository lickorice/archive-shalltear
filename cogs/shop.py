import discord, json, datetime, time
from discord.ext import commands
from data import db_users

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

start_time = time.time()

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class CoreCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def badgeshop(self, ctx):
        """This command shows the latency of the bot."""
        a = ctx.message.author
        with open('assets/obj_badgeshop.json') as f:
            badge_shop = json.load(f)
    
        
def setup(bot):
    bot.add_cog(CoreCog(bot))