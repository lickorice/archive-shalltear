import discord, math

class PaginatedEmbed:
    def __init__(self, owned_list, content_list, page_number, embed_type, max_pages):
        self.owned_list = owned_list
        self.content_list = content_list
        self.page_number = page_number
        self.embed_type = embed_type
        self.max_pages = max_pages

    def next_page(self):
        self.page_number = (self.page_number + 1) % self.max_pages

    def previous_page(self):
        self.page_number = (self.page_number - 1) % self.max_pages

    def get_embed(self):
        """Paginates your embeds. Returns an embed."""
        if self.embed_type == "bgshop":
            embed = discord.Embed(title="Backgrounds for Sale:", color=0xff1155)
            lower_bound = [i for i in range(0, len(self.content_list), 5)][self.page_number]
            for item in self.content_list[lower_bound:lower_bound+5]:
                print(item.id, self.owned_list, item.id in self.owned_list)
                if item.id in self.owned_list:
                    embed.add_field(
                        name="{} (Owned)".format(item.name),
                        value="~~`{0.price_tag}`~~\n`ID: {0.id}`".format(item),
                        inline=False
                        )
                else:
                    embed.add_field(
                        name=item.name,
                        value="`{0.price_tag}`\n`ID: {0.id}`".format(item),
                        inline=False
                        )
            if self.max_pages > 1:
                embed.set_footer(text="Page {}/{}".format(self.page_number+1, self.max_pages))
            return embed
        elif self.embed_type == "badgeshop":
            embed = discord.Embed(title="Badges for Sale:", color=0xff1155)
            lower_bound = [i for i in range(0, len(self.content_list), 5)][self.page_number]
            for item in self.content_list[lower_bound:lower_bound+5]:
                if item.id in self.owned_list:
                    embed.add_field(
                        name="{} (Owned)".format(item.name),
                        value="~~`{0.price_tag}`~~\n{0.description}".format(item),
                        inline=False
                        )
                else:
                    embed.add_field(
                        name=item.name,
                        value="`{0.price_tag}`\n{0.description}".format(item),
                        inline=False
                        )
            if self.max_pages > 1:
                embed.set_footer(text="Page {}/{}".format(self.page_number+1, self.max_pages))
            return embed

async def get_target_user(ctx, target_user):
    """Returns a User object on message mention, returns None if invalid."""
    if target_user != None:
        try:
            return ctx.message.mentions[0]
        except IndexError:
            await ctx.channel.send("**<@{}>, No such user found.**".format(ctx.message.author.id))
    else:
        return ctx.message.author

