import discord, sqlite3, datetime, time, json
from discord.ext import commands
from data import ldb

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

with open('assets/obj_help.json') as f:
    obj_help = json.load(f)
 
lkdb = ldb.LickDB()
start_time = time.time()


class Admin():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["h"])
    async def help(self, ctx, target_cmd=None):
        mstr = str_messages['str_invalid-cmd']
        if target_cmd is None:
            mstr = ''
            for cmd_group in obj_help:
                mstr += '__**{}**__:\n'.format(cmd_group)
                for cmd in obj_help[cmd_group]:
                    _name = cmd['name']
                    _desc = cmd['description']
                    mstr += '`{}`\n{}\n\n'.format(_name, _desc)
        else:
            for cmd_group in obj_help:
                for cmd in obj_help[cmd_group]:
                    _name = cmd['name']
                    _desc = cmd['description']
                    if target_cmd in cmd['cmd']:
                        mstr = '`{}`\n{}\n\n'.format(_name, _desc)
                        break
        await self.bot.say(mstr)

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        """This command is used to log out the bot, or shut it down."""
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say(str_messages['str_insuf-perms'])
            return
        await self.bot.say(str_messages['str_logging-out'])
        await self.bot.logout()

    @commands.command(pass_context=True)
    async def registerall(self, ctx):
        """This command is used to register all users into the database."""
        channel = ctx.message.channel
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say(str_messages['str_insuf-perms'])
            return
        m = await self.bot.say(str_messages['str_register-1'])
        svr = ctx.message.channel.server
        count, _count, bcount = 0, 0, 0
        for mbr in svr.members:
            count += 1
            if not mbr.bot:
                try:
                    lkdb.insertUser(mbr.id)
                    _count += 1
                except sqlite3.IntegrityError:
                    pass
            else:
                bcount += 1
            if count % 10 == 0:
                await self.bot.edit_message(m, str_messages['str_register-2'].format(_count, count))
        await self.bot.send_message(channel, str_messages['str_register-3'].format(_count, count, bcount))

    @commands.command(pass_context=True)
    async def setchannel(self, ctx, weight):
        """This command is used to set a channel's EXP gain rate."""
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say(str_messages['str_insuf-perms'])
            return
        chnID = ctx.message.channel.id
        lkdb.updateWeight(chnID, weight)
        lkdb.insertChannel(chnID, weight)

    @commands.command(pass_context=True)
    async def channelinfo(self, ctx):
        """This command is used to get a channel's EXP information."""
        chnID = ctx.message.channel.id
        embed = discord.Embed(title='#' + ctx.message.channel.name, color=0xff1155)
        embed.add_field(
            name="Experience gain",
            value=lkdb.getWeight(chnID)
        )
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, aliases=['info'])
    async def about(self, ctx):
        """This command is used to get the 'about' section of the bot."""
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime_str = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title=str_messages['str_about-title'], color=0xff1155)
        embed.add_field(
            name="Author",
            value=str_messages['str_author-name']
        )
        embed.add_field(
            name="Source Code",
            value=str_messages['str_src-link']
        )
        embed.add_field(
            name="Uptime",
            inline=False,
            value=uptime_str
        )
        embed.set_footer(text=str_messages['str_author-info'])
        await self.bot.send_message(ctx.message.channel, embed=embed)



def setup(bot):
    bot.add_cog(Admin(bot))
