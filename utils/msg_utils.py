async def get_target_user(ctx, target_user):
    if target_user != None:
        try:
            return ctx.message.mentions[0]
        except IndexError:
            await ctx.channel.send("**<@{}>, No such user found.**".format(ctx.message.author.id))
    else:
        return ctx.message.author