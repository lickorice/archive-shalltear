import discord, json, datetime
from discord.ext import commands
from data import db_users

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class XPCog:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        log(message)

        
def setup(bot):
    bot.add_cog(XPCog(bot))