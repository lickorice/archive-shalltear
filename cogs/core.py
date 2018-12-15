import discord, json, datetime, time, concurrent, tweepy
from conf import *
from modules.twitter import TwitterHelper
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

    @commands.command()
    @commands.cooldown(1, 120, type=commands.BucketType.user)
    async def twitter(self, ctx):
        """Follow the developer on Twitter to receive rewards!"""

        def check(m):
            try:
                return ctx.author.id == m.author.id and 0<=int(m.content)
            except:
                return False

        # TODO: Check if user already claimed rewards.
        
        twt = TwitterHelper()

        await ctx.send(f"**{ctx.author.display_name}**, authorize Shalltear in order to follow! {twt.get_url()}")
        try:
            await ctx.send("Simply send a message with the **authentication PIN**.")
            msg = await self.bot.wait_for('message', check=check, timeout=120)
        except concurrent.futures._base.TimeoutError:
            await ctx.channel.send(MSG_TIMEOUT.format(ctx.author.id))
            return
        try:
            if twt.authorize(msg.content):
                await ctx.send(f"<@{ctx.author.id}>, **you have successfully followed the developer!**")
            else:
                await ctx.send(f"<@{ctx.author.id}>, **you already follow the developer, processing rewards...**")
        
            # TODO: Process rewards here
        
        except tweepy.error.TweepError as e:
            await ctx.send(f"<@{ctx.author.id}>, **you have sent an invalid PIN. Try again after 2 minutes.**")
            print(e)
            return

        
def setup(bot):
    bot.add_cog(Core(bot))