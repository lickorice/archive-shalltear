import discord, sqlite3, datetime, time, json
from discord.ext import commands
from discord.utils import get
from data import ldb, linv

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

with open('assets/obj_badges.json') as f:
    obj_badges = json.load(f)
 
lkdb = ldb.LickDB()
invMan = linv.LickInventory()
invMan.init()
start_time = time.time()


class Shop():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def grantbadge(self, ctx, badgeID, userID=None):
        """This command is used to grant a user a badge."""
        if not ctx.message.author.server_permissions.administrator:
            await self.bot.say(str_messages['str_insuf-perms'])
            return
        if userID:
            try:
                a = ctx.message.mentions[0]
            except IndexError:
                a = get(ctx.message.channel.server.members, id=userID)
                if not a:
                    await self.bot.say(str_messages['str_user-not-found'])
                    return
        else:
            a = ctx.message.author

        invMan.init()

        if badgeID not in obj_badges["Badges"]:
            await self.bot.say(str_messages['str_badge-not-found'])
            return

        badgeName = obj_badges["Badges"][badgeID]["name"]

        if invMan.add_item(a.id, [badgeID, False]):
            await self.bot.say(str_messages['str_badge-grant-success'].format(a.id, badgeName))
        else:
            await self.bot.say(str_messages['str_badge-grant-failure'])

    @commands.command(pass_context=True)
    async def badges(self, ctx, param="status", badgeID=None):
        """This command is used to grant a user a badge."""
        a = ctx.message.author
        if param == "status":
            embed = discord.Embed(title="Current Badges - {}".format(a.name), color=0xff1155)
            equipped, unequipped = '', ''
            for badge in invMan.get_items(a.id):
                if badge[1] == False:
                    badgeName = obj_badges["Badges"][badge[0]]["name"]
                    unequipped += '`{}` // **{}**\n'.format(badge[0], badgeName)
                else:
                    badgeName = obj_badges["Badges"][badge[0]]["name"]
                    equipped += '`{}` // **{}**\n'.format(badge[0], badgeName)
            if len(equipped) == 0:
                equipped = "None"
            if len(unequipped) == 0:
                unequipped = "None"
            embed.add_field(
                name="Equipped Badges",
                value=equipped,
                inline=False
            )
            embed.add_field(
                name="Other Badges",
                value=unequipped,
                inline=False
            )
            await self.bot.send_message(ctx.message.channel, embed=embed)
        elif param == "equip":
            _badge = ''
            for _b in invMan.get_items(a.id):
                if _b[0] == badgeID:
                    _badge = _b
                    break

            result = invMan.equip_badge(a.id, _badge)

            if not result[0]:
                await self.bot.say(str_messages["str_invalid-cmd"])
            else:
                if result[1]:
                    await self.bot.say(str_messages["str_badge-equipped"].format(obj_badges["Badges"][badgeID]["name"]))
                else:
                    await self.bot.say(str_messages["str_badge-unequipped"].format(obj_badges["Badges"][badgeID]["name"]))


def setup(bot):
    bot.add_cog(Shop(bot))
