"""
A more specific database helper for the 'users' database.
To generate the database, use db_generate.py; also, this
helper inherits functions from the DBHelper class.

(coded by lickorice, 2018)
"""

import sqlite3
from data import db_helper
from conf import DATABASE_PATH

# Level config
base_exp, factor = 50, 1.5

class UserHelper(db_helper.DBHelper):
    def __init__(self, is_logged=True):
        self.database_path = './data/db/user.db'
        self.is_logged = is_logged

    def new_user(self, user_id, user_level=1, user_xp=0, user_xp_to_next=50, user_gil=10, user_materia=0):
        """Adds a new user to the database (user_id unique)."""
        try:
            self.insert_row(
                table_name="users",
                user_id=user_id,
                user_level=user_level,
                user_xp=user_xp,
                user_xp_to_next=user_xp_to_next,
                user_gil=user_gil,
                user_materia=0,
                user_bg_id=0
                )
        except sqlite3.IntegrityError:
            pass
        try:
            self.insert_row(
                table_name="activities",
                user_id=user_id,
                can_receive_xp=True,
                can_free_pack=True,
                can_daily=True,
                count_free_gil=0,
                count_commands=0,
                count_rolls=0,
                count_cards=0
                )
        except sqlite3.IntegrityError:
            pass
        try:
            self.insert_row(
                table_name="social",
                user_id=user_id,
                followed_twitter=False,
                followed_facebook=False,
                is_patron=False
                )
        except sqlite3.IntegrityError:
            pass

    def get_user(self, user_id):
        """Fetches user data given a user_id."""
        try:
            x = {
                "users": self.fetch_rows("users", user_id=user_id)[0],
                "activities": self.fetch_rows("activities", user_id=user_id)[0],
                "social": self.fetch_rows("social", user_id=user_id)[0]
                }
        except IndexError:
            return False
        return x

    def add_gil(self, user_id, value):
        """Adds gil to the user account (may be negative)."""
        self.increment_value(user_id, "users", "user_gil", value)

    def add_materia(self, user_id, value):
        """Adds materia to the user account (may be negative)."""
        self.increment_value(user_id, "users", "user_materia", value)

    def add_xp(self, user_id, value):
        """Adds xp to the user account (may be negative)."""
        self.increment_value(user_id, "users", "user_xp", value)
        user = self.get_user(user_id)
        if user["users"]["user_xp"] >= user["users"]["user_xp_to_next"]:
            return True
        return False

    def add_item(self, user_id, item_id, item_equipped=False):
        """Adds an item to the user account, given an id."""
        self.insert_row(
            table_name="inventory",
            owner_id=user_id,
            item_id=item_id,
            item_equipped=item_equipped
        )

    def add_bg(self, user_id, bg_id):
        """Adds a background to the user account, given an id."""
        self.insert_row(
            table_name="backgrounds",
            owner_id=user_id,
            bg_id=bg_id
        )

    def remove_item(self, user_id, item_id):
        """Removes an item from the user account, given an id."""
        self.remove_rows(
            table_name="inventory",
            owner_id=user_id,
            item_id=item_id
        )

    def check_item(self, user_id, item_id):
        """
        Returns False if the item exists in the account, else, 
        it returns the number of such items in the account.
        """
        item_query = self.fetch_rows(
            "inventory", True,
            owner_id=user_id,
            item_id=item_id
            )
        result = True if len(item_query) != 0 else len(item_query)
        return result

    def get_items(self, user_id, is_equipped=False):
        """
        Fetches all the items a user owns.
        Can be explicitly ordered to fetch only equipped items.
        """
        if is_equipped:
            return self.fetch_rows("inventory", True, owner_id=user_id, item_equipped=1)
        return self.fetch_rows("inventory", True, owner_id=user_id)

    def get_backgrounds(self, user_id):
        """
        Fetches all backgrounds the user owns.
        """
        return self.fetch_rows("backgrounds", True, owner_id=user_id)

    def toggle_item(self, user_id, item_id):
        """Toggles the equipped status of an item."""
        all_items = self.get_items(user_id)
        chosen_item = 'empty'
        for item in all_items:
            if item["item_id"] == item_id:
                chosen_item = item
                break
        if chosen_item == 'empty':
            return 3
        
        toggled = True if not item["item_equipped"] else False
        self.update_column(
            "inventory", 
            "item_equipped", 
            toggled, 
            owner_id=user_id, 
            item_id=item_id
            )
        if toggled:
            return 1
        return 2
    
    def change_bg(self, user_id, bg_id):
        """Changes the background (id) of the user."""
        self.update_column("users", "user_bg_id", bg_id, user_id=user_id)

    def next_level(self, user_id):
        """Automatically increments the user's level."""
        current_user = self.get_user(user_id)["users"]
        remainder_exp = current_user["user_xp"] - current_user["user_xp_to_next"]
        new_next = int(base_exp * ((current_user["user_level"]+1) ** factor))
        self.increment_value(user_id, "users", "user_level", 1)
        self.update_column("users", "user_xp", remainder_exp, user_id=user_id)
        self.update_column("users", "user_xp_to_next", new_next, user_id=user_id)

    def increment_value(self, user_id, table_name, column, value):
        """
        Automatically increments a certain value in the database.

        Args:
            user_id (int): The user ID of a discord User.
            table_name (str): The name of the table the column belongs to.
            column (str): The name of the column to be incremented.
            value (int): The value to be added (if positive) or subtracted (if otherwise).
        """
        # Utility function. Don't call directly.
        first_value = self.get_user(user_id)[table_name][column]
        self.update_column(table_name, column, (first_value+value), user_id=user_id)

    def add_lock(self, social_id, social_type):
        """
        Adds a lock to a certain user to prevent multiple Discord accounts
        from using a single social media account to accumulate rewards.

        Args:
            social_id (str): The ID of the user for the corresponding network
            social_type (str): The network of the user. ("TWT"/"FB")
        """
        try:
            self.insert_row(
                "social_lock",
                user_type = social_type,
                user_id = social_id+social_type
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def check_premium(self, user_id):
        x = self.fetch_rows("premium_users", True, user_id=user_id)
        return len(x) >= 1

    def add_premium(self, user_id):
        try:
            self.insert_row("premium_users", user_id=user_id)
            return True
        except sqlite3.IntegrityError:
            return False

    def rm_premium(self, user_id):
        self.remove_rows("premium_users", user_id=user_id)

def main():
    test = UserHelper(DATABASE_PATH+"user.db")
    x = test.connect()
    test.new_user(11)
    print(test.get_user(11)["users"])
    test.change_bg(11, 2)
    print(test.get_user(11)["users"])


if __name__ == '__main__':
    main()