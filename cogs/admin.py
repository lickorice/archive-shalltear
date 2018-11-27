import discord, json, datetime
from discord.ext import commands
from data import db_users

owner_id = 319285994253975553

with open("assets/str_msgs.json") as f:
    msg_strings = json.load(f)

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class AdminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['k'])
    async def kill(self, ctx):
        """Logout command (Owner)."""
        if ctx.author.id == owner_id:
            await self.bot.logout()
        else:
            await ctx.channel.send(msg_strings["str_insuf-perms"])

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

    @commands.command()
    async def registerall(self, ctx):
        """Adds all users (Owner)."""
        if ctx.author.id != owner_id:
            await ctx.channel.send(msg_strings["str_insuf-perms"])
        users_db = db_users.UserHelper()
        users_db.connect()
        for member in self.bot.get_all_members():
            users_db.new_user(member.id)
        users_db.close()


        
def setup(bot):
    bot.add_cog(AdminCog(bot))