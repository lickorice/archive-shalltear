import discord
from errors import *
from data import db_gacha
from objects.series import Series

types = {
    1: "Summoned",
    2: "Crafted",
    3: "Limited"
} # TODO: move this shit in config
rating = {
    1: "Common",
    2: "Uncommon",
    3: "Rare",
    4: "Mythical",
    5: "Legendary",
    6: "Divine"
}

class BoosterPack:
    """
    A BoosterPack wrapper to store cards.
    """
    def __init__(self, cards, user, page=0):
        self.cards = cards
        self.card_count = len(cards)
        self.user = user
        self.page = page

    def make_embed(self):
        current_card = self.cards[self.page]
        e = discord.Embed(title=current_card.name, color=0xff1155)
        e.set_image(url=current_card.full_url)

        # v = f"From **{current_card.series.name}**\n" # TODO: Make series objects
        v = f"From **{current_card.series.name}**\n"
        
        if current_card.is_exclusive:
            v += "**[IPM-Exclusive]**\n"

        v += f"Card Type: **{types[current_card.type]}**\n"
        v += f"Banish Gain: **{current_card.disenchant}** 💎 | Summon Cost: **{current_card.cost}** 💎\n"
        v += f"Acquired? **Yes, first by {current_card.first_user}**"

        e.add_field(name=rating[current_card.rating], value=v)
        e.set_footer(text=f"Page {self.page+1}/{self.card_count} (rolled by {self.user.name})")
        return e