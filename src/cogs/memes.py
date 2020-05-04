import discord, sqlite3, datetime, time, json, requests
from PIL import Image, ImageDraw
from discord.ext import commands
from discord.utils import get
from io import BytesIO
from conf import *

with open(ASSETS_DIRECTORY+'obj_memes.json') as f:
    obj_memes = json.load(f)

class Actor:
    def __init__(self, actor_list):
        x, y, size = actor_list
        self.x = x
        self.y = y
        self.size = size

class Meme:
    def __init__(self, meme_dict):
        self.url = meme_dict["FILE_URL"]
        self.actors = [Actor(a) for a in meme_dict["ACTORS"]]
 
class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.cooldown(1, 30, type=commands.BucketType.user)
    async def meme(self, ctx, meme_type=None, *target_users: discord.Member):
        """Generate memes!"""
        
        # get meme list:
        meme_str = ''
        for item in obj_memes:
            meme_str += '`{}` '.format(item)
        meme_str = meme_str.rstrip()

        # get a meme object!
        if meme_type == None:
            e = discord.Embed(title="Available Memes", color=0xff1155)
            e.add_field(name="Image Memes", value=meme_str, inline=True)
            await ctx.send(embed=e)
            return
        elif meme_type not in obj_memes:
            await ctx.send(MSG_MEME_NOT_FOUND)
            return
        
        # generate meme object
        _m = Meme(obj_memes[meme_type])

        # generate meme image
        meme_img = Image.open(ASSETS_DIRECTORY+f'memes/{_m.url}')

        required_actors = len(_m.actors)
        plurality = '' if required_actors == 1 else 's'
        if len(target_users) < required_actors:
            await ctx.send(MSG_MEME_NOT_ENOUGH.format(required_actors, plurality))
            return

        for index in range(required_actors):
            target_user = target_users[index]
            act = _m.actors[index]

            avatar_file = requests.get(target_user.avatar_url)
            avatar = Image.open(BytesIO(avatar_file.content))
            avatar = avatar.resize((act.size, act.size))
            meme_img.paste(avatar, (act.x, act.y))
            meme_img.save('temp/meme_temp.png')

        f = discord.File('temp/meme_temp.png')
        await ctx.send(file=f)

def setup(bot):
    bot.add_cog(Memes(bot))
