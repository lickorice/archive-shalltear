from discord.ext import commands
from conf import *

def is_owner():
    async def predicate(ctx):
        if ctx.author.id != OWNER_ID:
            await ctx.send(MSG_INSUF_PERMS)
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)