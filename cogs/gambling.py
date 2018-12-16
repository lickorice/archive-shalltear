import discord, json, datetime, concurrent, random, asyncio
from conf import *
from discord.ext import commands
from data import db_users, db_helper
from utils import msg_utils
from objects.user import User

current_tickets = {}

# Logging functions here:

def log(string):
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Start of program logic:

class Gambling:
    def __init__(self, bot):
        self.bot = bot

    async def drawtimer(self, ctx):
        await asyncio.sleep(60*5)
        await ctx.send("**Five minutes left until the lottery draw!**")
        await asyncio.sleep(60*2)
        await ctx.send("**Three minutes left until the lottery draw!**")
        await asyncio.sleep(60*2)
        await ctx.send("**One minute left until the lottery draw!**")
        await asyncio.sleep(50)
        await ctx.send("**Ten seconds left until the lottery draw!**")
        await asyncio.sleep(5)
        await ctx.send("**Five seconds left until the lottery draw!**")
        raw_tickets = current_tickets[ctx.guild.id]
        tickets = []
        for ticket in raw_tickets:
            entry = [ticket for i in range(raw_tickets[ticket])]
            tickets += entry
        random.shuffle(tickets)
        winner = self.bot.get_user(tickets[0])
        await ctx.send("Congratulations! <@{}> won the lottery and received **{} 💰** gil!".format(winner.id, (10+len(tickets)*2)))

        User(winner.id).add_gil((10+(len(tickets)*2)))

        current_tickets[ctx.guild.id] = {}

    @commands.command()
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
        ticket_list = ['{}\t**{}**'.format(self.bot.get_user(x[0]), x[1]) for x in ticket_tuples]
        jackpot = 10
        for i in ticket_dict:
            jackpot += 2*ticket_dict[i]
        # TODO: pagify this
        embed = discord.Embed(title="Tickets for {}".format(ctx.guild.name), color=CLR_MAIN_COLOR)
        embed.add_field(name="Jackpot", value='{} 💰 gil'.format(jackpot), inline=False)
        embed.add_field(name="Entries", value='\n'.join(ticket_list))
        await ctx.send(embed=embed)

    @commands.command(aliases=["lt"])
    async def lottery(self, ctx, tickets='1'):
        """
        Purchases a number (by default, one) tickets for the server-wide lottery.
        A winner is drawn every ten minutes.
        """
        _a = User(ctx.author.id)
        
        try:
            tickets = int(tickets)
        except ValueError:
            await ctx.send(MSG_INVALID_CMD)
            user_db.close()
            return

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
            test = current_tickets[ctx.guild.id]
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
    async def sweepstakes(self, ctx, number=None):
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
            try:
                lottery_entry = int(number)
            except ValueError:
                await ctx.channel.send(MSG_INVALID_CMD)

        # generate lottery:
        # TODO: Assign to JSON/py file, avoid hardcoding.
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