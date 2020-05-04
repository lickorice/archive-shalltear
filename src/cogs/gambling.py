import discord, json, datetime, concurrent, random, asyncio, math
from conf import *
from discord.ext import commands
from data import db_users, db_helper
from utils import msg_utils
from objects.user import User

refund_dict = {}
current_tickets = {}
stored_messages = {}

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == EMJ_LEFT_PAGE:
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == EMJ_RIGHT_PAGE:
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    async def on_reaction_remove(self, reaction, user):
        target_id = reaction.message.id
        if user.id not in stored_messages:
            return
        if target_id == stored_messages[user.id][0]:
            p = stored_messages[user.id][1]
            if reaction.emoji == EMJ_LEFT_PAGE:
                p.previous_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)
            elif reaction.emoji == EMJ_RIGHT_PAGE:
                p.next_page()
                e = p.get_embed()
                await reaction.message.edit(embed=e)

    async def drawtimer(self, ctx):
        count = 0
        while True:
            await asyncio.sleep(1)
            if count == 300:
                await ctx.send("**Five minutes left until the lottery draw!**")
            elif count == 420:
                await ctx.send("**Three minutes left until the lottery draw!**")
            elif count == 540:
                await ctx.send("**One minute left until the lottery draw!**")
            elif count == 590:
                await ctx.send("**Ten seconds left until the lottery draw!**")
            elif count == 595:
                await ctx.send("**Five seconds left until the lottery draw!**")
            elif count >= 600:
                break
            if current_tickets[ctx.guild.id] == {}:
                return # check for refunded tickets every second
            count += 1
        raw_tickets = current_tickets[ctx.guild.id]
        if current_tickets[ctx.guild.id] == {}:
            return
        tickets = []
        for ticket in raw_tickets:
            entry = [ticket for i in range(raw_tickets[ticket])]
            tickets += entry
        random.shuffle(tickets)
        winner = self.bot.get_user(tickets[0])
        await ctx.send("Congratulations! <@{}> won the lottery and received **{} 💰** gil!".format(winner.id, (3+len(tickets)*2)))

        User(winner.id).add_gil((3+(len(tickets)*2)))

        current_tickets[ctx.guild.id] = {}
        refund_dict[ctx.guild.id]  = []

    @commands.command(aliases=['vr'])
    @commands.guild_only()
    async def voterefund(self, ctx):
        global current_tickets
        global refund_dict
        try:
            ticket_dict = current_tickets[ctx.guild.id]
        except KeyError:
            await ctx.send("**No one has sent any tickets yet in this server**")
        if ctx.author.id not in ticket_dict:
            await ctx.send(f"**{ctx.author.display_name}, you don't even have tickets in this server.**")
            return
        try:
            if ctx.author.id in refund_dict[ctx.guild.id]:
                await ctx.send(f"**You already voted for a refund for this server.**")
                return
            else:
                refund_dict[ctx.guild.id].append(ctx.author.id)
        except KeyError:
            refund_dict[ctx.guild.id] = [ctx.author.id]
        if len(refund_dict[ctx.guild.id]) >= len(ticket_dict):
            await ctx.send("**Lottery successfully cancelled. Refunding tickets...**")
            for user_id in ticket_dict:
                _u = User(user_id)
                _u.add_gil((ticket_dict[user_id]*2))
            current_tickets[ctx.guild.id]  = {}
            refund_dict[ctx.guild.id]  = []
            return
        else:
            votecount = f'{len(refund_dict[ctx.guild.id])} / {len(ticket_dict)} votes'
            await ctx.send(f"**{ctx.author.display_name}, you have successfully voted for a refund.** `{votecount}`")
            return

    @commands.command(aliases=['tix'])
    @commands.cooldown(2, 10, type=commands.BucketType.user)
    @commands.guild_only()
    async def tickets(self, ctx):
        """Views the current tickets in the server's lottery."""
        try:
            ticket_dict = current_tickets[ctx.guild.id]
            if len(ticket_dict) == 0:
                await ctx.send("**No one has sent any tickets yet in this server.**")
        except KeyError:
            await ctx.send("**No one has sent any tickets yet in this server.**")
            return
        ticket_tuples = [(user_id, ticket_dict[user_id]) for user_id in ticket_dict]
        ticket_tuples = sorted(ticket_tuples, key=lambda x: x[1])[::-1]
        ticket_list = ['{} **{}** tix'.format(self.bot.get_user(x[0]), x[1]) for x in ticket_tuples]
        jackpot = 3
        for i in ticket_dict:
            jackpot += 2*ticket_dict[i]

        # generate the embed
        max_pages = math.ceil(len(ticket_list) / 10)
        p = msg_utils.PaginatedEmbed(
            [], ticket_list, 0, "tix", max_pages,
            guild=ctx.guild.name, jackpot='{} 💰 gil'.format(jackpot)
        )
        embed = p.get_embed()

        msg = await ctx.send(embed=embed)
        
        stored_messages[ctx.author.id] = (msg.id, p)

        if max_pages > 1:
            await msg.add_reaction(EMJ_LEFT_PAGE)
            await msg.add_reaction(EMJ_RIGHT_PAGE)

    @commands.command(aliases=["lt"])
    @commands.cooldown(2, 10, type=commands.BucketType.user)
    @commands.guild_only()
    async def lottery(self, ctx, tickets: int=1):
        """
        Purchases a number (by default, one) tickets for the server-wide lottery.
        A winner is drawn every ten minutes.
        """
        _a = User(ctx.author.id)

        if _a.gil < (tickets*2):
            await ctx.send(MSG_INSUF_GIL)
            return

        if tickets <= 0:
            await ctx.send(MSG_AM_I_A_JOKE.format(ctx.author.id))
            return

        _a.add_gil(-(tickets*2))

        p = '' if tickets == 1 else 's'
        await ctx.send("**{}**, you successfully bought **{} ticket{}** for **{} 💰 gil**.".format(ctx.author.display_name, tickets, p, tickets*2))
        try:
            _trash = current_tickets[ctx.guild.id]
        except KeyError:
            current_tickets[ctx.guild.id] = {}
        if len(current_tickets[ctx.guild.id]) == 0:
            current_tickets[ctx.guild.id] = {ctx.author.id: tickets}
            await self.drawtimer(ctx)
        else:
            if ctx.author.id in current_tickets[ctx.guild.id]:
                current_tickets[ctx.guild.id][ctx.author.id] += tickets
            else:
                current_tickets[ctx.guild.id][ctx.author.id] = tickets

    @commands.command(aliases=['sspot'])
    @commands.cooldown(2, 10, type=commands.BucketType.user)
    @commands.guild_only()
    async def stakespot(self, ctx):
        """Shows the current lottery jackpot."""
        helper_db = db_helper.DBHelper("data/db/misc.db", False)
        helper_db.connect()
        try:
            current_pot = helper_db.fetch_rows(
                "lottery", strict=True,
                guild_id=ctx.guild.id
            )[0]["pot_amount"]
        except IndexError:
            helper_db.insert_row("lottery", guild_id=ctx.guild.id, pot_amount=0)
            current_pot = 0
        await ctx.channel.send(MSG_SWEEPSTAKES_POT.format(current_pot))

    @commands.command(aliases=['ss'])
    @commands.cooldown(2, 10, type=commands.BucketType.user)
    @commands.guild_only()
    async def sweepstakes(self, ctx, number: int=None):
        """Take your chances with the sweepstakes!"""
        author = ctx.message.author

        _a = User(author.id)

        if _a.gil < 2:
            await ctx.channel.send(MSG_INSUF_GIL)
            user_db.close()
            return

        def check(m):
            try:
                return author.id == m.author.id and 0<=int(m.content)<=999
            except:
                return False

        if number==None:
            await ctx.channel.send(MSG_SWEEPSTAKES_NO.format(author.display_name))
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=10)
            except concurrent.futures._base.TimeoutError:
                await ctx.channel.send(MSG_TIMEOUT.format(author.id))
                return
            lottery_entry = int(msg.content)
        else:
            lottery_entry = number

        # generate lottery:
        numdict = {1:"one", 2:"two", 3: "three", 4:"four",
        5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine", 0:"zero"}
        string = [i for i in "❓❓❓"]
        msg = await ctx.channel.send(''.join(string))
        num_total = 0
        for i in range(3):
            current_number = random.randint(0, 9)
            string[i] = ':{}:'.format(numdict[current_number])
            await msg.edit(content=''.join(string))
            num_total += current_number*(10**(2-i))

        if num_total == lottery_entry:
            helper_db = db_helper.DBHelper("data/db/misc.db", False)
            helper_db.connect()
            try:
                current_pot = helper_db.fetch_rows(
                    "lottery", strict=True,
                    guild_id=ctx.guild.id
                )[0]["pot_amount"] + 2
            except IndexError:
                helper_db.insert_row("lottery", guild_id=ctx.guild.id, pot_amount=0)
                current_pot = 2
            helper_db.update_column("lottery", "pot_amount", 0, guild_id=ctx.guild.id)
            helper_db.close()

            await ctx.channel.send(MSG_SWEEPSTAKES_WIN.format(author.id, current_pot))

            user_db = db_users.UserHelper(False)
            _a.add_gil(current_pot)

        else:
            user_db = db_users.UserHelper(False)
            _a.add_gil(-2)

            helper_db = db_helper.DBHelper("data/db/misc.db", False)
            helper_db.connect()
            try:
                current_pot = helper_db.fetch_rows(
                    "lottery", strict=True,
                    guild_id=ctx.guild.id
                )[0]["pot_amount"]
                helper_db.update_column("lottery", "pot_amount", current_pot+2, guild_id=ctx.guild.id)
            except IndexError:
                helper_db.insert_row("lottery", guild_id=ctx.guild.id, pot_amount=2)
            helper_db.close()
            await ctx.channel.send(MSG_SWEEPSTAKES_LOSS.format(author.display_name))
            

def setup(bot):
    bot.add_cog(Gambling(bot))