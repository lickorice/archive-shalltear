import discord, sqlite3, datetime, time, json, requests
from PIL import Image, ImageDraw
from discord.ext import commands
from discord.utils import get
from data import ldb
from io import BytesIO

with open('assets/str_msgs.json') as f:
    str_messages = json.load(f)

with open('assets/obj_memes.json') as f:
    obj_memes = json.load(f)
 
lkdb = ldb.LickDB()
start_time = time.time()


class Memes():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['m'])
    async def meme(self, ctx, meme_type=None, *user_targets):
        """This command is used to generate memes!"""

        # get meme list:
        meme_str = ''
        for item in obj_memes:
            meme_str += '`{}` '.format(item)
        meme_str = meme_str.rstrip()

        # get a meme object!
        if meme_type == None:
            embed = discord.Embed(title="Available Memes", color=0xff1155)
            embed.add_field(name="Image Memes", value=meme_str, inline=True)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            return
        elif meme_type not in obj_memes:
            await self.bot.say(str_messages["str_meme-not-found"])
            return
        
        # generate meme object
        meme_obj = obj_memes[meme_type]
        print(meme_obj)

        # generate meme image
        meme_img = Image.open('assets/memes/{}'.format(meme_obj["FILE_URL"]))

        required_actors = len(meme_obj["ACTORS"])
        plurality = '' if required_actors == 1 else 's'
        if len(user_targets) < required_actors:
            await self.bot.say(str_messages["str_meme-not-enough"].format(required_actors, plurality))
            return

        if len(ctx.message.mentions) < required_actors:
            await self.bot.say(str_messages["str_user-not-found"])
            return

        for index in range(required_actors):
            raw_id = user_targets[index]
            user_id = raw_id[3:-1] if raw_id.startswith('<@!') else raw_id[2:-1]
            target_user = get(ctx.message.channel.server.members, id=user_id)
            # target_user = ctx.message.mentions[index]
            # print(target_user, user_id)
            x, y, size = meme_obj["ACTORS"][index]
            # print(x, y, size)

            avatar_file = requests.get(target_user.avatar_url)
            avatar = Image.open(BytesIO(avatar_file.content))
            avatar = avatar.resize((size, size), Image.BILINEAR)
            meme_img.paste(avatar, (x, y))

        meme_img.save('temp/meme_temp.png')
        await self.bot.send_file(ctx.message.channel, 'temp/meme_temp.png')

def setup(bot):
    bot.add_cog(Memes(bot))
