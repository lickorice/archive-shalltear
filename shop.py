import discord, sqlite3, datetime, time, json
from discord.ext import commands
from discord.utils import get
from data import ldb, linv

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

with open('assets/obj_badges.json') as f:
    obj_badges = json.load(f)

with open('assets/obj_shop.json') as f:
    obj_shop = json.load(f)

VIP_ROLE_ID = "443742098705874944"
VIP_CHANNEL = "442677527115464705"
 
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
    async def shop(self, ctx):
        """This command is used to access the shop."""
        embed = discord.Embed(title="Shop Items", color=0xff1155)
        for entry in obj_shop["Shop"]:
            embed.add_field(
                name=entry["name"],
                value='`id:` **{}**\n`price:` **{}**\n{}\n'.format(entry["id"], entry["price-tag"], entry["desc"]),
                inline=True
            )
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def buy(self, ctx, itemID):
        """This command is used to buy a shop item."""
        author = ctx.message.author
        shopItem = False
        for item in obj_shop["Shop"]:
            if item["id"] == itemID:
                shopItem = item
                break
        if not shopItem:
            await self.bot.say(str_messages["str_item-not-found"])
            return
        if invMan.check_item(itemID, author.id):
            await self.bot.say(str_messages["str_badge-already-exists"])
            return
        if lkdb.getCash(author.id) < shopItem["price"]:
            await self.bot.say(str_messages["str_insuf-gil"])
            return
        if lkdb.getLvl(author.id) < shopItem["level-needed"]:
            await self.bot.say(str_messages["str_insuf-lvl"])
            return
        lkdb.updateCash(author.id, -shopItem["price"])
        invMan.add_item(author.id, [itemID, True])
        await self.bot.say("<@{}>, you have successfully bought **{}**.".format(author.id, shopItem["name"]))

        # vip special
        print (shopItem)
        print (shopItem["id"])
        if shopItem["id"] == "00000":
            print("Fulfilled!")
            role = get(ctx.message.channel.server.roles, id=VIP_ROLE_ID)
            channel = get(ctx.message.channel.server.channels, id=VIP_CHANNEL)
            print(role, channel)
            await self.bot.add_roles(author, role)
            await self.bot.send_message(channel, str_messages["str_vip-welcome"].format(author.id))
        else:
            print("Not fulfilled!", shopItem["id"], "00000")


    @commands.command(pass_context=True)
    async def badges(self, ctx, param="status", badgeID=None):
        """
        By default or by using `status`, the command shows your current badges.
        Using `equip` will toggle if they are shown in your profile.
        """
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
