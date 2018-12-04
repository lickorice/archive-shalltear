import discord, json, datetime
from discord.ext import commands
from data import db_users

owner_id = 319285994253975553 # Lickorice

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class CoreCog:
    def __init__(self, bot):
        self.bot = bot
        
    async def on_command_error(self, ctx, error):
        if type(error) == type(discord.ext.commands.errors.CommandNotFound()):
            return
        await ctx.channel.send(msg_strings["str_cmd-error"].format(ctx.message.author.id, error))

    @commands.command(aliases=['info'])
    async def about(self, ctx):
        """This command shows information about the bot."""
        embed = discord.Embed(title=msg_strings['str_about-title'], color=0xff1155)
        embed.add_field(
            name="Author",
            value=msg_strings['str_author-name']
        )
        embed.add_field(
            name="Source Code",
            value=msg_strings['str_src-link']
        )
        embed.set_footer(text=msg_strings['str_author-info'])
        await ctx.channel.send(embed=embed)

    async def on_member_join(self, member):
        if member.bot:
            return
        log("[-EVT-] New user joined. ({})".format(member.name))
        users_db = db_users.UserHelper()
        if not users_db.connect():
            log("[-ERR-] Database failed to connect.")
        users_db.new_user(member.id)
        users_db.close()
    
        
def setup(bot):
    bot.add_cog(CoreCog(bot))