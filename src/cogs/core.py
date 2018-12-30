import discord, json, datetime, time, concurrent, tweepy
from conf import *
from utils import msg_utils
from modules.twitter import TwitterHelper
from objects.user import User
from discord.ext import commands
from data import db_users

start_time = time.time()

allowed_errors = [
    discord.ext.commands.errors.CommandOnCooldown,
    discord.ext.commands.errors.MissingRequiredArgument,
    discord.ext.commands.errors.BadArgument,
    discord.ext.commands.errors.NoPrivateMessage
]

caught_errors = [
    discord.ext.commands.errors.CommandNotFound,
    discord.ext.commands.errors.CheckFailure
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
            if type(error) == discord.ext.commands.errors.CommandOnCooldown:
                await ctx.send(MSG_CMD_ERROR.format(ctx.author.id, error))
            elif type(error) == discord.ext.commands.errors.NoPrivateMessage:
                await ctx.send(MSG_CMD_NODMS)
            else:
                await ctx.send(MSG_INVALID_CMD)
        elif type(error) in caught_errors:
            log(f"[-WRN-] {ctx.author.name} raised an error: {error}")
        else:
            raise error

    async def on_member_join(self, member):
        if member.bot:
            return
        log("[-EVT-] New user joined. ({})".format(member.name))
        u = User(member.id)

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """Shows the latency of the bot."""
        await ctx.channel.send(MSG_PING.format(int(round(self.bot.latency, 3) * 1000)))

    @commands.command()
    async def help(self, ctx, command=None):
        """Shows all the features the bot is able to do."""
        all_commands = [cmd for cmd in self.bot.commands]
        if command == None:
            embed = discord.Embed(title="Commands for Shalltear", color=0xff1155)
            for cog in self.bot.cogs:
                commands_for_cog = [f'`{c.name}`' for c in all_commands if not c.hidden and c.cog_name == cog]
                s = ' '.join(commands_for_cog)
                embed.add_field(name=cog, inline=False, value=s)
            await ctx.send("Do `s!help <command>` for more information.")
        else:
            if command not in [c.name for c in all_commands]:
                await ctx.send(MSG_CMD_NOT_FOUND.format(ctx.author.id))
                return
            cmd = [c for c in all_commands if c.name == command][0]
            if cmd.aliases:
                name = f'{cmd.name} [{"/".join(cmd.aliases)}]'
            else:
                name = cmd.name
            if cmd.clean_params:
                name += f' <{", ".join(cmd.clean_params)}>'
            name = '`{}`'.format(name)
            embed = discord.Embed(title=cmd.cog_name, color=0xff1155)
            embed.add_field(name=name, value=cmd.help)
        await ctx.send(embed=embed)
            

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
        embed.add_field(
            name="Version",
            value=CURRENT_VERSION
        )
        embed.set_footer(text=MSG_AUTHOR_INFO)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Invite Shalltear to your server!"""
        try:
            await ctx.author.send(MSG_BOT_INVITE.format(BOT_INVITE_LINK))
            await ctx.send(MSG_DM_SENT.format(ctx.author.display_name))
        except discord.errors.Forbidden:
            await ctx.send(MSG_BLOCKED.format(ctx.author.id))
            return

    @commands.command()
    async def donate(self, ctx):
        """Donate to the developer!"""
        await ctx.send(MSG_BOT_DONATE.format(BOT_INVITE_LINK))
        return

    @commands.command()
    async def exclusive(self, ctx):
        """Get an invite to the exclusive server for Shalltear!"""
        try:
            await ctx.author.send(MSG_EXCLUSIVE_SERVER.format(OWNER_GUILD_INVITE))
            await ctx.send(MSG_DM_SENT.format(ctx.author.display_name))
        except discord.errors.Forbidden:
            await ctx.send(MSG_BLOCKED.format(ctx.author.id))
            return

    @commands.command()
    @commands.cooldown(1, 300, type=commands.BucketType.user)
    async def twitter(self, ctx):
        """Follow the developer on Twitter to receive rewards!"""

        def check(m):
            try:
                return ctx.author.id == m.author.id and 0<=int(m.content)
            except:
                return False

        twt = TwitterHelper()

        _user = User(ctx.author.id)

        if _user.followed_twitter:
            await ctx.author.send(MSG_REWARDS_1.format(ctx.author.display_name))
            return

        try:
            await ctx.author.send(MSG_TWITTER_AUTH.format(ctx.author.display_name, twt.get_url()))
            await ctx.send(MSG_DM_SENT.format(ctx.author.display_name))
        except discord.errors.Forbidden:
            await ctx.send(MSG_BLOCKED.format(ctx.author.id))
            return

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=300)
        except concurrent.futures._base.TimeoutError:
            await ctx.channel.send(MSG_TIMEOUT.format(ctx.author.id))
            return
        try:
            r = twt.authorize(msg.content) 
            if r == 1:
                await ctx.author.send(f"<@{ctx.author.id}>, **you have successfully followed the developer!**")
            elif r == 2:
                await ctx.author.send(f"<@{ctx.author.id}>, **you already follow the developer, processing rewards...**")
            elif r == 3:
                await ctx.author.send(MSG_REWARDS_2.format(ctx.author.display_name))
                return
            
            await ctx.send(MSG_GIL_RECEIVED.format(
                ctx.author.id, 500, "following **@cgpanganiban** on Twitter"
            ))
            await ctx.send(MSG_BADGE_RECEIVED.format(
                ctx.author.id, "Twitter"
            ))
            _user.add_gil(500)
            _user.followed_twitter = True
            _user.add_badge(8)

        except tweepy.error.TweepError as e:
            await ctx.author.send(f"<@{ctx.author.id}>, **you have sent an invalid PIN. Try again after 5 minutes.**")
            print(e)
            return

        
def setup(bot):
    bot.add_cog(Core(bot))