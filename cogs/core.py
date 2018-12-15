import discord, json, datetime, time
from conf import *
from discord.ext import commands
from data import db_users

start_time = time.time()

allowed_errors = [
    type(discord.ext.commands.errors.CommandOnCooldown(0, 0))
]

caught_errors = [
    type(discord.ext.commands.errors.CommandNotFound())
]

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Core:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if type(error) in allowed_errors:
            await ctx.send(MSG_CMD_ERROR.format(ctx.author.id, error))
        elif type(error) in caught_errors:
            log(f"[-WRN-] {ctx.author.name} raised an error: {error}")
        else:
            raise error

    @commands.command()
    async def ping(self, ctx):
        """Shows the latency of the bot."""
        await ctx.channel.send(MSG_PING.format(int(round(self.bot.latency, 3) * 1000)))

    @commands.command(aliases=['info'])
    async def about(self, ctx):
        """Shows information about the bot."""
        difference = int(round(time.time() - start_time))
        uptime_str = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title=MSG_ABOUT_TITLE, color=CLR_MAIN_COLOR)
        embed.add_field(
            name="Author",
            value=MSG_AUTHOR_NAME
        )
        embed.add_field(
            name="Source Code",
            value=MSG_SRC_LINK
        )
        embed.add_field(
            name="Uptime",
            value=uptime_str,
            inline=False
        )
        embed.set_footer(text=MSG_AUTHOR_INFO)
        await ctx.channel.send(embed=embed)

    async def on_member_join(self, member):
        if member.bot:
            return
        log("[-EVT-] New user joined. ({})".format(member.name))
        user_db = db_users.UserHelper()
        if not user_db.connect():
            log("[-ERR-] Database failed to connect.")
        user_db.new_user(member.id)
        user_db.close()
    
        
def setup(bot):
    bot.add_cog(Core(bot))