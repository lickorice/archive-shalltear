async def get_target_user(ctx, target_user):
    """Returns a User object on message mention, returns None if invalid."""
    if target_user != None:
        try:
            return ctx.message.mentions[0]
        except IndexError:
            await ctx.channel.send("**<@{}>, No such user found.**".format(ctx.message.author.id))
    else:
        return ctx.message.author

async def paginate(msg, msg_list, msg_interval, embed_type):
    """Paginates your embeds."""
    pass