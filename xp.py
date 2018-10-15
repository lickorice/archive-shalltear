import discord, datetime, asyncio, json, requests, profiler, sqlite3
from PIL import Image
from discord.ext import commands
from discord.utils import get
from data import ldb
from io import BytesIO

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

img_offset = 24, 24
img_temp = Image.open('assets/img_level-up-template.png')
bg_temp = Image.new('RGBA', (52, 52), (44, 47, 51, 255))
bg2_temp = Image.open('assets/background-1.png')

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
                    await self.bot.say(str_messages['str_user-not-found'])
                    return
        else:
            a = ctx.message.author
        chn = ctx.message.channel
        try:
            profiler.generate(a.name, a.avatar_url, lkdb.getLvl(a.id), (lkdb.getExp(a.id), lkdb.getTarg(a.id)))
            await self.bot.send_file(chn, 'temp/profile.png')
        except Exception as e:
            print("ERROR! - {}".format(e))

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
                if cur == 0:
                    return
            except TypeError as e:
                print(e)
                try:
                    print("New user detected.")
                    lkdb.insertUser(a.id)
                    cur = lkdb.updateExp(a.id, lkdb.getWeight(message.channel.id))
                except sqlite3.IntegrityError:
                    pass
            targetExp = lkdb.getTarg(a.id)
            if cur >= targetExp:
                cur -= targetExp
                newlvl = lkdb.updateLvl(a.id, residual=cur)
                
                # generate the image:
                imgfile = requests.get(a.avatar_url)
                pfp = Image.open(BytesIO(imgfile.content))
                pfp = pfp.resize((52, 52), Image.BICUBIC)
                bg_temp.paste(pfp, (0, 0))
                img_temp.paste(bg_temp, img_offset, mask=bg_temp)
                bg2_temp.paste(img_temp, (0,0), mask=img_temp)
                bg2_temp.save('temp/levelup.png')
                
                m = await self.bot.send_file(message.channel, 'temp/levelup.png')
                await asyncio.sleep(10)
                await self.bot.delete_message(m)
            print(a.name, '\t', cur, targetExp)


def setup(bot):
    bot.add_cog(Xp(bot))
