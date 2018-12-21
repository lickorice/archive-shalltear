from data import db_gacha
from objects.card import Card

class Gacha(object):
    """A wrapper for Shalltear's gacha system per user."""
    def __init__(self, user):
        self.db = db_gacha.GachaHelper(False)
        self.owner_id = user.id

    def add_card(self, card):
        """Add a card to a user's Gacha inventory"""
        self.db.connect()
        self.db.add_card_to_inventory(card, self.owner_id)
        self.db.close()

    @property
    def cards(self):
        # fetch cards from the gacha database
        self.db.connect()
        result = self.db.get_user_cards(self.owner_id)
        self.db.close()
        return result