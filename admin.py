import discord
from discord.ext import commands
from data import ldb
import sqlite3

lkdb = ldb.LickDB()


class Admin():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say("**Insufficient permissions.**")
            return
        await self.bot.say("**Logging out...**")
        await self.bot.logout()

    @commands.command(pass_context=True)
    async def registerAll(self, ctx):
        channel = ctx.message.channel
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say("**Insufficient permissions.**")
            return
        m = await self.bot.say("**Attempting to register users...**")
        svr = ctx.message.channel.server
        count, _count, bcount = 0, 0, 0
        for mbr in svr.members:
            count += 1
            # print(mbr.id, mbr.bot)  # debug print
            if not mbr.bot:
                try:
                    lkdb.insertUser(mbr.id)
                    print("Successfully registered {}.".format(mbr.id))
                    _count += 1
                except sqlite3.IntegrityError:
                    print("User already exists.")
            else:
                bcount += 1
            if count % 10 == 0:
                await self.bot.edit_message(m, "**Attempting to register users...\n({}/{})**".format(_count, count))
        await self.bot.send_message(channel, "**{}** of **{}** users successfully registered. ".format(_count, count)+"Out of all **{}** users, **{}** are bots.".format(count, bcount))

    @commands.command(pass_context=True)
    async def setchannel(self, ctx, weight):
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say("**Insufficient permissions.**")
            return
        chnID = ctx.message.channel.id
        lkdb.updateWeight(chnID, weight)
        lkdb.insertChannel(chnID, weight)

    @commands.command(pass_context=True)
    async def channelinfo(self, ctx):
        chnID = ctx.message.channel.id
        embed = discord.Embed(title='#' + ctx.message.channel.name, color=0xff1155)
        embed.add_field(
            name="Experience gain",
            value=lkdb.getWeight(chnID)
        )
        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
