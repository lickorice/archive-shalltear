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
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say("**Insufficient permissions.**")
            return
        await self.bot.say("**Attempting to register users...**")
        svr = ctx.message.channel.server
        count, _count, bcount = 0, 0, 0
        for mbr in svr.members:
            count += 1
            # print(mbr.id, mbr.bot)  # debug print
            if not mbr.bot:
                try:
                    lkdb.insertUser(mbr.id)
                    print("Successfully registered {}.".format(mbr.name))
                    _count += 1
                except sqlite3.IntegrityError:
                    print("User already exists.")
            else:
                bcount += 1
        await self.bot.say("**{}** of **{}** users successfully registered. "
                           .format(_count, count) +
                           "Out of all **{}** users, **{}** are bots."
                           .format(count, bcount))


def setup(bot):
    bot.add_cog(Admin(bot))
