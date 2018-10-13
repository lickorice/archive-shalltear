from discord.ext import commands
from discord.utils import get
from data import ldb
import sqlite3, random, asyncio, json

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

lkdb = ldb.LickDB()
# costs:
costs = {
    'slot_machine': 3
}
# ids:
id = {
    'licko': '319285994253975553'
}


class Economy():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['ql'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def quick(self, ctx):
        """Quick lottery game."""
        cost = costs['slot_machine']
        if lkdb.getCash(ctx.message.author.id) < cost:
            mstr = "**Not enough money to play. Quick Lotto costs 2 💰.**"
            await self.bot.say(mstr)
            return
        lkdb.updateCash(ctx.message.author.id, -2)
        x = random.randint(0, 10000000)
        if x <= 1:
            lkdb.updateCash(ctx.message.author.id, 5000)
            mstr = "**JACKPOT!!! {}, you won 5000 💰! @everyone**".format(ctx.message.author.name)
            await self.bot.say(mstr)
        elif 2 <= x <= 6:
            lkdb.updateCash(ctx.message.author.id, 2500)
            mstr = "**YEET!! {}, you won 2500 💰!**".format(ctx.message.author.name)
            await self.bot.say(mstr)
        elif 7 <= x <= 16:
            lkdb.updateCash(ctx.message.author.id, 1500)
            mstr = "**DAMN! {}, you won 1500 💰!**".format(ctx.message.author.name)
            await self.bot.say(mstr)
        elif 17 <= x <= 100016:
            lkdb.updateCash(ctx.message.author.id, 10)
            mstr = "**Congratulations {}, you won 10 💰!**".format(ctx.message.author.name)
            await self.bot.say(mstr)
        elif 100017 <= x <= 2500000:
            lkdb.updateCash(ctx.message.author.id, 5)
            mstr = "**Congratulations {}, you won 5 💰!**".format(ctx.message.author.name)
            await self.bot.say(mstr)
        elif 2500001 <= x <= 7500000:
            lkdb.updateCash(ctx.message.author.id, 2)
            mstr = "**{}**, you won back 2 💰!".format(ctx.message.author.name)
            await self.bot.say(mstr)
        elif 7500001 <= x:
            lkdb.updateCash(ctx.message.author.id, 0)
            mstr = "**{}**, sadly, you lost.".format(ctx.message.author.name)
            await self.bot.say(mstr)

    @commands.command(pass_context=True)
    async def grant(self, ctx, target_user=None, cash=0):
        """This command is used to grant a user money."""
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say(str_messages['str_insuf-perms'])
            return
        if target_user:
            try:
                a = ctx.message.mentions[0]
            except IndexError:
                a = get(ctx.message.channel.server.members, id=target_user)
                if not a:
                    await self.bot.say(str_messages['str_user-not-found'])
                    return
        else:
            a = ctx.message.author
        lkdb.updateCash(a.id, int(cash))
        if cash >= 0:
            mstr = str_messages['str_grant-positive'].format(a.id, a.name, int(cash))
        else:
            mstr = str_messages['str_grant-negative'].format(a.id, abs(int(cash)))
        await self.bot.say(mstr)

    @commands.command(pass_context=True)
    async def grantall(self, ctx, cash=0):
        """This command is used to grant all users money."""
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say(str_messages['str_insuf-perms'])
            return
        if cash >= 0:
            mstr = str_messages['str_grant-all-positive'].format(int(cash))
            await self.bot.say(mstr)
        else:
            mstr = str_messages['str_grant-all-negative'].format(abs(int(cash)))
            await self.bot.say(mstr)
        for mbr in ctx.message.channel.server.members:
            if mbr.bot:
                continue
            print(mbr.id, mbr.name)
            lkdb.updateCash(mbr.id, cash)

    @commands.command(pass_context=True)
    async def give(self, ctx, target_user=None, cash=0):
        """This command is used to give a user a certain amount of money."""
        if target_user:
            try:
                a = ctx.message.mentions[0]
            except IndexError:
                a = get(ctx.message.channel.server.members, id=target_user)
                if not a:
                    await self.bot.say(str_messages['str_user-not-found'])
                    return
        else:
            return
        _a = ctx.message.author
        if cash <= 0:
            mstr = str_messages['str_invalid-amount'].format(_a.id)
            await self.bot.say(mstr)
            return
        if lkdb.getCash(_a.id) < cash:
            mstr = str_messages['str_insuf-funds'].format(_a.id)
            return
        lkdb.updateCash(_a.id, cash*-1)
        lkdb.updateCash(a.id, cash)
        mstr = str_messages['str_give'].format(a.id, cash, _a.id)
        await self.bot.say(mstr)

    @commands.command(pass_context=True, aliases=['$', 'balance', 'money'])
    async def gil(self, ctx, target_user=None):
        """This command is used to display a user's money."""
        if target_user:
            try:
                a = ctx.message.mentions[0]
            except IndexError:
                a = get(ctx.message.channel.server.members, id=target_user)
                if not a:
                    await self.bot.say(str_messages['str_user-not-found'])
                    return
        else:
            a = ctx.message.author

        await self.bot.say(str_messages['str_balance'].format(a.id, lkdb.getCash(a.id)))

    async def on_command_error(self, error, ctx):
        """This function is used to handle commands on cooldown."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            mstr = str_messages['str_cmd-error'].format(ctx.message.author.id, error)
            m = await self.bot.send_message(ctx.message.channel, mstr)
            await asyncio.sleep(5)
            self.bot.delete_message(m)


def setup(bot):
    bot.add_cog(Economy(bot))
