from data import db_gacha
from objects.card import Card

class Gacha(object):
    """A wrapper for Shalltear's gacha system."""
    def __init__(self, user):
        self.db = db_gacha.GachaHelper(False)
        self.user = user # Pass User object here

    @property
    def cards(self):
        # fetch cards from the gacha database
        self.db.connect()
        all_card_ids = self.db.get_user_cards(self.user.id)
        result = [Card(card_id) for card_id in all_card_ids]
        self.db.close()
        return result