from data import db_gacha
from objects.series import Series

class Card:
    """
    A Card object to store information about a Card within
    a User's gacha inventory.

    Args:
        card_id (int): The corresponding ID for the card
    
    Attributes:
        name (str): The name of the card
        img_url (str): The URL of the card's image
        rating (int): The rarity rating of the card (1-6)
        creates_cards (list): List of Cards that the card is able to create
        created_by (list): List of Cards needed to create this card
        can_be_drawn (bool): If the card appears naturally in Gacha draws
        salvage_cost (int): The materia gained upon destroying the card
        creation_cost (int): The materia needed to create the card (25x of salvage)
            A value of 0 means the Card is not able to be reproduced using materia
            Defaults to 0 if the Card does not appear in draws (can_be_drawn)
    """
    def __init__(self, card_id):
        self.id = card_id
        # fetch db-based details of card here
        db = db_gacha.GachaHelper(False)
        db.connect()
        # self.name
        # self.img_url
        # self.rating
        # self.creates_cards
        # self.created_by
        # self.can_be_drawn
        # self.salvage_cost
        # self.creation_cost = 0 if self.can_be_drawn > 0 self.salvage_cost * 10
        
        # series-related attr:
        # self.series
        db.close()
