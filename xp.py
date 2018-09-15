import discord
from discord.ext import commands
from discord.utils import get
from data import ldb
import datetime
import asyncio

lkdb = ldb.LickDB()
doctxt = "developed by Lickorice | Carlos Panganiban | cgpanganiban@up.edu.ph"
xptime = {"user": 0}
epoch = datetime.datetime.utcfromtimestamp(0)

cooldown = 3  # seconds of exp cooldown


class Xp():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def profile(self, ctx, target_user=None):
        """This shows a user's profile, given an ID or a mention."""
        if target_user:
            try:
                a = ctx.message.mentions[0]
            except IndexError:
                a = get(ctx.message.channel.server.members, id=target_user)
                if not a:
                    await self.bot.say("**No such user found.**")
                    return
        else:
            a = ctx.message.author
        chn = ctx.message.channel
        embed = discord.Embed(title="Profile", color=0xff1155)
        embed.add_field(
            name="Name",
            value=a.name,
            inline=True
        )
        embed.add_field(
            name="Level",
            value=lkdb.getLvl(a.id),
            inline=True
        )
        embed.add_field(
            name="Experience",
            value=lkdb.getExp(a.id),
            inline=True
        )
        embed.add_field(
            name="EXP needed for next level",
            value=lkdb.getTarg(a.id),
            inline=True
        )
        embed.add_field(
            name="Gil",
            value=str(lkdb.getCash(a.id)) + ' 💰',
            inline=True
        )
        embed.set_thumbnail(url=a.avatar_url)
        embed.set_footer(text=doctxt)
        await self.bot.send_message(chn, embed=embed)

    async def on_message(self, message):
        """Updates exp and level per user."""
        if message.author.bot:
            return

        a = message.author

        try:
            curtime = xptime[a.id]
        except KeyError:
            xptime[a.id] = 0

        curtime = xptime[a.id]
        cursecs = (datetime.datetime.utcnow()-epoch).total_seconds()
        time_diff = cursecs-curtime
        if time_diff >= cooldown:
            xptime[a.id] = (datetime.datetime.utcnow() - epoch).total_seconds()
            try:
                cur = lkdb.updateExp(a.id, lkdb.getWeight(message.channel.id))
            except TypeError:
                return
            targetExp = lkdb.getTarg(a.id)
            if cur >= targetExp:
                cur -= targetExp
                newlvl = lkdb.updateLvl(a.id, residual=cur)
                embed = discord.Embed(title="Level Up!", color=0xff1155)
                embed.add_field(
                    name="Name",
                    value=a.name,
                    inline=True
                )
                embed.add_field(
                    name="Level",
                    value=newlvl,
                    inline=True
                )
                embed.set_thumbnail(url=a.avatar_url)
                m = await self.bot.send_message(message.channel, embed=embed)
                await asyncio.sleep(10)
                await self.bot.delete_message(m)
            print(a.id, cur, targetExp)


def setup(bot):
    bot.add_cog(Xp(bot))
