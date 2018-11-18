import discord, sqlite3, datetime, time, json, random
from discord.utils import get
from discord.ext import commands
from data import gachadb, ldb

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

with open('assets/str_types.json') as f:
    raw = json.load(f)
    card_ratings = raw["RATINGS"]
    card_types= raw["TYPES"]

with open('assets/tab_gacha-series.json') as f:
    raw = json.load(f)
    card_series = {int(series_id): raw[series_id] for series_id in raw}
 
gdb = gachadb.GachaDB()
ldb = ldb.LickDB()
start_time = time.time()

last_hour = 100

pack_price = 10

prob_setting = {
    1: 32,
    2: 16,
    3: 4,
    4: 2,
    5: 1
}

card_price = {
    0: 1,
    1: 2,
    2: 5,
    3: 7,
    4: 10,
    5: 50
}

class Gacha():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['fc'])
    async def freecards(self, ctx):
        """This command is used to roll for cards."""

        global last_hour
        a = ctx.message.author

        # last_hour = 100 # uncomment for no cooldowns

        current_hour = datetime.datetime.now().hour
        # what to do after an hour:
        if last_hour != current_hour:
            last_hour = current_hour
            gdb.clear_cooldown()
        if not gdb.put_on_cooldown(a.id):
            minutes_left = 60 - datetime.datetime.now().minute
            plurality = 's' if minutes_left != 1 else ''
            await self.bot.say(str_messages["str_on-cooldown"].format(
                a.name, minutes_left, plurality
            ))
            return
        
        all_cards = gdb.fetch_all_cards()

        card_total = 0
        card_index = []
        for card in all_cards:
            card_total += prob_setting[card["RATING"]]
            card_index.extend([card["ID"] for i in range(prob_setting[card["RATING"]])])
        
        card_results = []

        for i in range(3):
            index = random.randrange(card_total)
            card_id = card_index[index]
            card_results.append(gdb.fetch_card(card_id))
            gdb.insert_card(a.id, card_id)

        for card in card_results:
            e = discord.Embed(color=0xff1155, title="You got a new card!")
            e.set_image(url=card["IMG"])
            e.add_field(
                name="{}".format(card["NAME"]),
                value="{}\n{}\n{}\nID:\t{}\n{}".format("⭐"*card["RATING"], '**{}**'.format(card_ratings[card["RATING"]]), card_series[card["SERIES_ID"]],  card["ID"], card_types[card["CARD_TYPE"]]),
                inline=False
            )
            e.set_footer(text="Rolled by {}".format(a.name), icon_url=a.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=e)


    @commands.command(pass_context=True, aliases=['bc'])
    async def buycards(self, ctx):
        """This command is used to roll for cards."""

        global pack_price
        a = ctx.message.author

        user_cash = ldb.getCash(a.id)
        if user_cash < pack_price:
            await self.bot.say(str_messages["str_gacha-insuf-funds"].format(a.name, pack_price))
            return

        ldb.updateCash(a.id, -pack_price)
        await self.bot.say(str_messages["str_gacha-funds-deduct"].format(a.name, pack_price))
        
        all_cards = gdb.fetch_all_cards()

        card_total = 0
        card_index = []
        for card in all_cards:
            card_total += prob_setting[card["RATING"]]
            card_index.extend([card["ID"] for i in range(prob_setting[card["RATING"]])])
        
        card_results = []

        for i in range(3):
            index = random.randrange(card_total)
            card_id = card_index[index]
            card_results.append(gdb.fetch_card(card_id))
            gdb.insert_card(a.id, card_id)

        for card in card_results:
            e = discord.Embed(color=0xff1155, title="You got a new card!")
            e.set_image(url=card["IMG"])
            e.add_field(
                name="{}".format(card["NAME"]),
                value="{}\n{}\n{}\nID:\t{}\n{}".format("⭐"*card["RATING"], '**{}**'.format(card_ratings[card["RATING"]]), card_series[card["SERIES_ID"]],  card["ID"], card_types[card["CARD_TYPE"]]),
                inline=False
            )
            e.set_footer(text="Rolled by {}".format(a.name), icon_url=a.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=e)


    @commands.command(pass_context=True, aliases=['mc'])
    async def mycards(self, ctx):
        """This command is used to see cards."""

        a = ctx.message.author

        all_cards = gdb.get_all_cards(a.id)

        card_str = ''

        for card in sorted(all_cards):
            card_object = gdb.fetch_card(card[0])
            card_str += '{} {}\n'.format(card_object["NAME"], "★"*card_object["RATING"])

        card_str = card_str.rstrip()

        e = discord.Embed(color = 0xff1155, title="{}'s Inventory".format(a.name))
        e.add_field(
            name='All Cards ({})'.format(len(all_cards)),
            value= card_str
        )

        await self.bot.send_message(ctx.message.channel, embed=e)

    @commands.command(pass_context=True, aliases=['vc'])
    async def viewcard(self, ctx, *target_card):
        """This command is used to see cards."""

        a = ctx.message.author

        target_card = ' '.join(target_card)

        card = gdb.fetch_card(target_card)
        if card == False:
            await self.bot.say(str_messages["str_gacha-card-dne"].format(a.name))
            return

        e = discord.Embed(color=0xff1155, title="Search Results")
        e.set_image(url=card["IMG"])
        e.add_field(
            name="{}".format(card["NAME"]),
            value="{}\n{}\n{}\nID:\t{}\n{}".format("⭐"*card["RATING"], '**{}**'.format(card_ratings[card["RATING"]]), card_series[card["SERIES_ID"]],  card["ID"], card_types[card["CARD_TYPE"]]),
            inline=False
        )
        await self.bot.send_message(ctx.message.channel, embed=e)

    @commands.command(pass_context=True, aliases=['vs'])
    async def viewseries(self, ctx, *target_series):
        """This command is used to fetch series."""

        a = ctx.message.author

        target_series = ' '.join(target_series)

        id_found = -1
        for series_id in card_series:
            if card_series[series_id].lower() == target_series.lower():
                id_found = series_id
                break

        if id_found == -1:
            await self.bot.say(str_messages["str_gacha-series-dne"].format(a.name))
            return

        all_cards = gdb.fetch_all_cards(seriesID=series_id)

        card_str = ''
        for card in all_cards:
            card_str += '{} {}\n'.format(card["NAME"], '★'*card["RATING"])
        card_str = card_str.rstrip()

        e = discord.Embed(color=0xff1155, title="Search Results")
        e.add_field(
            name="{}".format(card_series[id_found]),
            value=card_str,
            inline=False
        )

        await self.bot.send_message(ctx.message.channel, embed=e)

    @commands.command(pass_context=True, aliases=['sc'])
    async def sellcard(self, ctx, *target_card):
        """This command is used to sell cards."""
        a = ctx.message.author

        target_card = ' '.join(target_card)

        card_selected = gdb.fetch_card(target_card)
        if card_selected == False:
            await self.bot.say(str_messages["str_gacha-card-dne"].format(a.name))
            return

        if gdb.sell_card(a.id, card_selected["ID"]):
            await self.bot.say(str_messages["str_gacha-sell-succ"].format(a.name, card_selected["NAME"], card_price[card_selected["RATING"]]))
            ldb.updateCash(a.id, card_price[card_selected["RATING"]])
            return
        else:
            await self.bot.say(str_messages["str_gacha-sell-fail"].format(a.name))
            return

    @commands.command(pass_context=True, aliases=['sd'])
    async def selldupes(self, ctx):
        """This command is used to sell card duplicates in inventory."""

        a = ctx.message.author

        all_cards = gdb.get_all_cards(a.id)



def setup(bot):
    bot.add_cog(Gacha(bot))
