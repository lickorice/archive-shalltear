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
    2: 3,
    3: 5,
    4: 7,
    5: 20
}

temp_embed_messages = {}

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
                value="{}\n{}\n{}\nID:\t{}\n{}".format("⭐"*card["RATING"], '**{}**'.format(card_ratings[card["RATING"]]), card_series[card["SERIES_ID"]][0],  card["ID"], card_types[card["CARD_TYPE"]]),
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
                value="{}\n{}\n{}\nID:\t{}\n{}".format("⭐"*card["RATING"], '**{}**'.format(card_ratings[card["RATING"]]), card_series[card["SERIES_ID"]][0],  card["ID"], card_types[card["CARD_TYPE"]]),
                inline=False
            )
            e.set_footer(text="Rolled by {}".format(a.name), icon_url=a.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=e)


    @commands.command(pass_context=True, aliases=['mc'])
    async def mycards(self, ctx, target_user=None):
        """This command is used to see cards."""

        author = ctx.message.author

        if target_user != None:
            a = ctx.message.mentions[0]
        elif target_user == None or a == None:
            a = ctx.message.author

        all_cards = gdb.get_all_cards(a.id)

        if len(all_cards) == 0:
            await self.bot.say("**{}**, you currently don't have any cards. Redeem one with **s!fc**.".format(a.name))
            return

        ranges = [(i, i+10) for i in range(0, len(all_cards), 10)]
        pages = [i for i in range(1, len(ranges)+1)]

        current_page = 0

        # generate embed:
        card_str = ''

        for card in sorted(all_cards)[ranges[current_page][0]:ranges[current_page][1]]:
            card_object = gdb.fetch_card(card[0])
            card_str += '{} {}\n'.format(card_object["NAME"], "★"*card_object["RATING"])

        card_str = card_str.rstrip()

        e = discord.Embed(color = 0xff1155, title="{}'s Inventory".format(a.name))
        e.add_field(
            name='All Cards ({})'.format(len(all_cards)),
            value= card_str
        )
        e.set_footer(
            text="Page {}/{}".format(pages[current_page], max(pages))
        )

        msg = await self.bot.send_message(ctx.message.channel, embed=e)
        
        if max(pages) != 1:
            await self.bot.add_reaction(msg, '◀')
            await self.bot.add_reaction(msg, '▶')
        temp_embed_messages[author.id] = [msg, all_cards, current_page, a.id, "mc"]

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
            value="{}\n{}\n{}\nID:\t{}\n{}".format("⭐"*card["RATING"], '**{}**'.format(card_ratings[card["RATING"]]), card_series[card["SERIES_ID"]][0],  card["ID"], card_types[card["CARD_TYPE"]]),
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
            if card_series[series_id][0].lower() == target_series.lower():
                id_found = series_id
                break

        if id_found == -1:
            await self.bot.say(str_messages["str_gacha-series-dne"].format(a.name))
            return

        all_cards = gdb.fetch_all_cards(seriesID=id_found)

        ranges = [(i, i+10) for i in range(0, len(all_cards), 10)]
        pages = [i for i in range(1, len(ranges)+1)]

        current_page = 0

        owned_cards = gdb.get_all_cards(a.id)
        owned_cards = [card[0] for card in owned_cards]

        owned_count = len(['a' for card in all_cards if card["ID"] in owned_cards])

        card_str = ''
        for card in all_cards[ranges[current_page][0]:ranges[current_page][1]]:
            if card["ID"] in owned_cards:
                card_str += '~~***{} {}***~~\n'.format(card["NAME"], '★'*card["RATING"])
                continue
            card_str += '{} {}\n'.format(card["NAME"], '★'*card["RATING"])
        card_str = card_str.rstrip()

        e = discord.Embed(color=0xff1155, title="Search Results")
        e.set_thumbnail(url=card_series[id_found][1])
        e.add_field(
            name="{} ({}/{})".format(card_series[id_found][0], owned_count, len(all_cards)),
            value=card_str,
            inline=False
        )
        e.set_footer(
            text="Page {}/{}".format(pages[current_page], max(pages))
        )

        msg = await self.bot.send_message(ctx.message.channel, embed=e)
        if max(pages) != 1:
            await self.bot.add_reaction(msg, '◀')
            await self.bot.add_reaction(msg, '▶')
        temp_embed_messages[a.id] = [msg, all_cards, current_page, id_found, "vs"]

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

        # check dupes
        card_ids = [card[0] for card in all_cards]
        dupe_ids = {card_id: -1 for card_id in card_ids if card_ids.count(card_id) > 1}


        for card_id in card_ids:
            if card_ids.count(card_id) > 1:
                dupe_ids[card_id] += 1

        if len(dupe_ids) == 0:
            await self.bot.say(str_messages["str_gacha-no-dupe"].format(a.name))
            return

        dupes, total_value = 0, 0
        for card_id in dupe_ids:
            for iterations in range(dupe_ids[card_id]):
                dupes += 1
                price = card_price[gdb.fetch_card(card_id)["RATING"]]
                total_value += price
                ldb.updateCash(a.id, price)
                gdb.sell_card(a.id, card_id)

        plurality = 's' if dupes != 1 else ''
        await self.bot.say(str_messages["str_gacha-yes-dupe"].format(a.name, dupes, plurality, total_value))

    @commands.command(pass_context=True, aliases=['t'])
    async def trade(self, ctx, target_user):
        """This command is used to trade cards."""
        a = ctx.message.author
        b = ctx.message.mentions[0]

        if a.id == b.id:
            await self.bot.say("Nice try, kiddo ;)")
            return

        a_card_selected = None
        b_card_selected = None

        all_cards = gdb.fetch_all_cards()
        all_cards = {card["NAME"].lower(): card["ID"] for card in all_cards}
        all_owned_ids = gdb.get_all_cards(a.id)
        all_owned_ids = [card[0] for card in all_owned_ids]

        if b == None:
            await self.bot.say(str_messages["str_user-not-found"])
            return
        
        await self.bot.say("**<@{}>**, please enter card name you want to trade:".format(a.id))
        
        # wait for message
        while True:
            trade_proposal = await self.bot.wait_for_message(timeout=10, author=a)

            if trade_proposal == None:
                await self.bot.say("Trade has timed out after 10 seconds. Cancelling...")
                return

            if trade_proposal.content.lower().startswith('s!'):
                continue

            if trade_proposal.content.lower() not in all_cards:
                await self.bot.say(str_messages["str_gacha-card-dne"].format(a.name))
                continue

            if all_cards[trade_proposal.content.lower()] not in all_owned_ids:
                await self.bot.say(str_messages["str_gacha-sell-fail"].format(a.name))
                continue
            else:
                a_card_selected = gdb.fetch_card(all_cards[trade_proposal.content.lower()])
                break;

        all_owned_ids = gdb.get_all_cards(b.id)
        all_owned_ids = [card[0] for card in all_owned_ids]

        await self.bot.say("**<@{}>**, please enter card name you want to trade:".format(b.id))
        # wait for message
        while True:
            trade_proposal = await self.bot.wait_for_message(timeout=10, author=b)

            if trade_proposal == None:
                await self.bot.say("Trade has timed out after 10 seconds. Cancelling...")
                return

            if trade_proposal.content.lower() not in all_cards:
                await self.bot.say(str_messages["str_gacha-card-dne"].format(b.name))
                continue

            if all_cards[trade_proposal.content.lower()] not in all_owned_ids:
                await self.bot.say(str_messages["str_gacha-sell-fail"].format(b.name))
                continue
            else:
                b_card_selected = gdb.fetch_card(all_cards[trade_proposal.content.lower()])
                break;

        await self.bot.say("<@{}>, **{}** wants to trade **{}** for **{}**. Do you accept? **(y/n)**".format(a.id, b.name, b_card_selected["NAME"], a_card_selected["NAME"]))
        # wait for message
        while True:
            response = await self.bot.wait_for_message(timeout=10, author=a)
            if response.content.lower() == 'y':
                await self.bot.say("**Trade accepted**. **{}** has been exchanged for **{}**.".format(a_card_selected["NAME"], b_card_selected["NAME"]))
                gdb.sell_card(a.id, a_card_selected["ID"])
                gdb.sell_card(b.id, b_card_selected["ID"])
                gdb.insert_card(a.id, b_card_selected["ID"])
                gdb.insert_card(b.id, a_card_selected["ID"])
                return
            elif response.content.lower() == 'n':
                await self.bot.say("**Trade cancelled.**")
                return
            else:
                await self.bot.say("**Invalid response.** Try again.")
                continue

    @commands.command(pass_context=True, aliases=['gc'])
    async def givecard(self, ctx, target_user, *card_name):
        """This command is used to trade cards."""

        a = ctx.message.author
        b = ctx.message.mentions[0]

        if a.id == b.id:
            await self.bot.say("Lol.")
            return

        card_name = ' '.join(card_name)
        card_selected = gdb.fetch_card(card_name)
        owner_cards = gdb.get_all_cards(a.id)
        owner_cards = [card[0] for card in owner_cards]
        if card_selected["ID"] not in owner_cards:
            await self.bot.say(str_messages["str_gacha-sell-fail"].format(a.name))
            return

        await self.bot.say("<@{}> are you sure you want to give **{}** to <@{}>? **(y/n)**".format(a.id, card_selected["NAME"], b.id))

        while True:
            response = await self.bot.wait_for_message(timeout=10, author=a)
            if response.content.lower() == 'y':
                await self.bot.say("**{}** has been given to **{}**.".format(card_selected["NAME"], b.name))
                gdb.sell_card(a.id, card_selected["ID"])
                gdb.insert_card(b.id, card_selected["ID"])
                return
            elif response.content.lower() == 'n':
                await self.bot.say("**Successfully cancelled.**")
                return
            else:
                await self.bot.say("**Invalid response.** Try again.")
                continue

    async def on_reaction_add(self, reaction, user):

        if user.bot:
            return

        a = user

        if a.id not in temp_embed_messages:
            return
            if reaction.message != temp_embed_messages[a.id][0]:
                return

        msg, all_cards, current_page, og_id, m_type = temp_embed_messages[a.id]

        if reaction.emoji == '▶':
            current_page += 1
        elif reaction.emoji == '◀':
            current_page -= 1
        else:
            return

        ranges = [(i, i+10) for i in range(0, len(all_cards), 10)]
        pages = [i for i in range(1, len(ranges)+1)]

        current_page %= max(pages)

        # generate embed:
        card_str = ''

        if m_type == 'mc':
            
            for card in sorted(all_cards)[ranges[current_page][0]:ranges[current_page][1]]:
                card_object = gdb.fetch_card(card[0])
                card_str += '{} {}\n'.format(card_object["NAME"], "★"*card_object["RATING"])

            card_str = card_str.rstrip()

            b = get(reaction.message.channel.server.members, id=og_id)
            e = discord.Embed(color = 0xff1155, title="{}'s Inventory".format(b.name))
            e.add_field(
                name='All Cards ({})'.format(len(all_cards)),
                value= card_str
            )
        elif m_type == 'vs':

            owned_cards = gdb.get_all_cards(a.id)
            owned_cards = [card[0] for card in owned_cards]

            owned_count = len(['a' for card in all_cards if card["ID"] in owned_cards])

            for card in all_cards[ranges[current_page][0]:ranges[current_page][1]]:
                if card["ID"] in owned_cards:
                    card_str += '~~***{} {}***~~\n'.format(card["NAME"], '★'*card["RATING"])
                    continue
                card_str += '{} {}\n'.format(card["NAME"], '★'*card["RATING"])
            card_str = card_str.rstrip()

            e = discord.Embed(color=0xff1155, title="Search Results")
            e.set_thumbnail(url=card_series[og_id][1])
            e.add_field(
                name="{} ({}/{})".format(card_series[og_id][0], owned_count, len(all_cards)),
                value=card_str,
                inline=False
            )
        e.set_footer(
            text="Page {}/{}".format(pages[current_page], max(pages))
        )

        await self.bot.edit_message(msg, embed=e)
        
        temp_embed_messages[a.id][2] = current_page

    async def on_reaction_remove(self, reaction, user):

        if user.bot:
            return

        a = user

        if a.id not in temp_embed_messages:
            return
            if reaction.message != temp_embed_messages[a.id][0]:
                return

        msg, all_cards, current_page, og_id, m_type = temp_embed_messages[a.id]

        if reaction.emoji == '▶':
            current_page += 1
        elif reaction.emoji == '◀':
            current_page -= 1
        else:
            return

        ranges = [(i, i+10) for i in range(0, len(all_cards), 10)]
        pages = [i for i in range(1, len(ranges)+1)]

        current_page %= max(pages)

        # generate embed:
        card_str = ''

        if m_type == 'mc':
            
            for card in sorted(all_cards)[ranges[current_page][0]:ranges[current_page][1]]:
                card_object = gdb.fetch_card(card[0])
                card_str += '{} {}\n'.format(card_object["NAME"], "★"*card_object["RATING"])

            card_str = card_str.rstrip()

            b = get(reaction.message.channel.server.members, id=og_id)
            e = discord.Embed(color = 0xff1155, title="{}'s Inventory".format(b.name))
            e.add_field(
                name='All Cards ({})'.format(len(all_cards)),
                value= card_str
            )
        elif m_type == 'vs':

            owned_cards = gdb.get_all_cards(a.id)
            owned_cards = [card[0] for card in owned_cards]

            owned_count = len(['a' for card in all_cards if card["ID"] in owned_cards])

            for card in all_cards[ranges[current_page][0]:ranges[current_page][1]]:
                if card["ID"] in owned_cards:
                    card_str += '~~***{} {}***~~\n'.format(card["NAME"], '★'*card["RATING"])
                    continue
                card_str += '{} {}\n'.format(card["NAME"], '★'*card["RATING"])
            card_str = card_str.rstrip()

            e = discord.Embed(color=0xff1155, title="Search Results")
            e.set_thumbnail(url=card_series[og_id][1])
            e.add_field(
                name="{} ({}/{})".format(card_series[og_id][0], owned_count, len(all_cards)),
                value=card_str,
                inline=False
            )
        e.set_footer(
            text="Page {}/{}".format(pages[current_page], max(pages))
        )

        await self.bot.edit_message(msg, embed=e)
        
        temp_embed_messages[a.id][2] = current_page


def setup(bot):
    bot.add_cog(Gacha(bot))
