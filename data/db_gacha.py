"""
A more specific database helper for the 'gacha' database.
To generate the database, use db_generate.py; also, this
helper inherits functions from the DBHelper class.

(coded by lickorice, 2018)
"""

from data import db_helper
from errors import *
from modules import google
from objects.card import Card

class GachaHelper(db_helper.DBHelper):
    def __init__(self, is_logged=True):
        self.database_path = 'data/db/gacha.db'
        self.is_logged = is_logged

    def new_card(self, card):
        """Adds a new card to the database (card_id unique)."""
        self.insert_row(
            table_name="cards",
            card_id=card.id,
            card_name=card.name,
            card_type=card.type,
            card_rating=card.rating,
            card_points=card.points,
            card_cost=card.cost,
            card_disenchant=card.disenchant,
            card_full_url=card.full_url,
            card_icon_url=card.icon_url,
            card_series_id=card.series_id,
            card_is_flagship=card.is_flagship,
            card_acquired=card.acquired,
            card_user=card.first_user,
            card_submitter=card.submitter,
            is_exclusive=card.is_exclusive
            )

    def consolidate_cards(self):
        """Recreate the database according to Google Sheets content."""
        cards = google.get_all_cards()
        # set_config = google.get_all_sets() # TODO: Concretize this
        # TODO: Create a backup of the database
        self.delete_all_rows('cards')
        for card in cards:
            self.new_card(Card.get_from_dict(card))
        return len(cards)

    def get_card(self, card_id):
        x = self.fetch_rows('cards', True, card_id=card_id)
        if len(x) == 0:
            raise CardNotFound(f"{card_id} not found in the database")
        return Card.get_from_db(x[0])

    def get_card_from_name(self, card_name):
        x = self.fetch_rows('cards', False, card_name=card_name)
        if len(x) == 0:
            raise CardNotFound(f"{card_name} not found in the database")
        return Card.get_from_db(x[0])

    def get_all_cards(self, key=lambda x: x.id):
        """Returns a list of all cards, sorted with a key."""
        x = self.fetch_rows('cards')
        x = [Card.get_from_db(row) for row in x]
        x = sorted(x, key=key)
        return x 

    # def add_card(self, user_id, card_id):
    #     """Adds a card to a user's inventory."""
    #     pass

    # def get_progress(self, user_id, series_id):
    #     """Returns a user's progress for a series."""
    #     pass

    # def add_xp(self, user_id, value):
    #     """Adds xp to the user account (may be negative)."""
    #     self.increment_value(user_id, "users", "user_xp", value)
    #     user = self.get_user(user_id)
    #     if user["users"]["user_xp"] >= user["users"]["user_xp_to_next"]:
    #         return True
    #     return False

    # def add_item(self, user_id, item_id, item_equipped=False):
    #     """Adds an item to the user account, given an id."""
    #     self.insert_row(
    #         table_name="inventory",
    #         owner_id=user_id,
    #         item_id=item_id,
    #         item_equipped=item_equipped
    #     )

    # def add_bg(self, user_id, bg_id):
    #     """Adds a background to the user account, given an id."""
    #     self.insert_row(
    #         table_name="backgrounds",
    #         owner_id=user_id,
    #         bg_id=bg_id
    #     )

    # def remove_item(self, user_id, item_id):
    #     """Removes an item from the user account, given an id."""
    #     self.remove_rows(
    #         table_name="inventory",
    #         owner_id=user_id,
    #         item_id=item_id
    #     )

    # def check_item(self, user_id, item_id):
    #     """
    #     Returns False if the item exists in the account, else, 
    #     it returns the number of such items in the account.
    #     """
    #     item_query = self.fetch_rows(
    #         "inventory", True,
    #         owner_id=user_id,
    #         item_id=item_id
    #         )
    #     result = True if len(item_query) != 0 else len(item_query)
    #     return result

    # def get_items(self, user_id, is_equipped=False):
    #     """
    #     Fetches all the items a user owns.
    #     Can be explicitly ordered to fetch only equipped items.
    #     """
    #     if is_equipped:
    #         return self.fetch_rows("inventory", True, owner_id=user_id, item_equipped=1)
    #     return self.fetch_rows("inventory", True, owner_id=user_id)

    # def get_backgrounds(self, user_id):
    #     """
    #     Fetches all backgrounds the user owns.
    #     """
    #     return self.fetch_rows("backgrounds", True, owner_id=user_id)

    # def toggle_item(self, user_id, item_id):
    #     """Toggles the equipped status of an item."""
    #     all_items = self.get_items(user_id)
    #     chosen_item = 'empty'
    #     for item in all_items:
    #         if item["item_id"] == item_id:
    #             chosen_item = item
    #             break
    #     if chosen_item == 'empty':
    #         return 3
        
    #     toggled = True if not item["item_equipped"] else False
    #     self.update_column(
    #         "inventory", 
    #         "item_equipped", 
    #         toggled, 
    #         owner_id=user_id, 
    #         item_id=item_id
    #         )
    #     if toggled:
    #         return 1
    #     return 2
    
    # def change_bg(self, user_id, bg_id):
    #     """Changes the background (id) of the user."""
    #     self.update_column("users", "user_bg_id", bg_id, user_id=user_id)

    # def next_level(self, user_id):
    #     """Automatically increments the user's level."""
    #     current_user = self.get_user(user_id)["users"]
    #     remainder_exp = current_user["user_xp"] - current_user["user_xp_to_next"]
    #     new_next = int(base_exp * ((current_user["user_level"]+1) ** factor))
    #     self.increment_value(user_id, "users", "user_level", 1)
    #     self.update_column("users", "user_xp", remainder_exp, user_id=user_id)
    #     self.update_column("users", "user_xp_to_next", new_next, user_id=user_id)

    def increment_value(self, user_id, table_name, column, value):
        """
        Automatically increments a certain value in the database.

        Args:
            user_id (int): The user ID of a discord User.
            table_name (string): The name of the table the column belongs to.
            column (string): The name of the column to be incremented.
            value (int): The value to be added (if positive) or subtracted (if otherwise).
        """
        # Utility function. Don't call directly.
        first_value = self.get_user(user_id)[table_name][column]
        self.update_column(table_name, column, (first_value+value), user_id=user_id)


def main():
    print("You are running the bare version of db_gacha.py.")
    print("This will refresh everything in the cards table.")
    test = GachaHelper()



if __name__ == '__main__':
    main()