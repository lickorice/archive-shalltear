from data import db_users, db_gacha
from objects.background import Background
from objects.badge import Badge
from objects.gacha import Gacha

class User:
    """
    Self-defined User object containing most of Shalltear-
    essential attributes and methods.

    Args:
        user_id (int): The Discord user's ID.

    Attributes:
        id (int): The Discord user's ID.
        db (data.db_users.UserHelper): The current UserHelper instance
            to help with database operations.
    """
    def __init__(self, user_id):
        self.id = user_id
        self.db = db_users.UserHelper(is_logged=False)
        self.is_registered()

    @property
    def is_premium(self):
        self.db.connect()
        x = self.db.check_premium(self.id)
        self.db.close()
        return x

    def toggle_premium(self):
        if self.is_premium:
            self.db.connect()
            self.db.rm_premium(self.id)
            self.db.close()
            return False
        else:
            self.db.connect()
            self.db.add_premium(self.id)
            self.db.close()
            return True

    @property
    def gacha(self):
        return Gacha(self)

    @property
    def bg_id(self):
        return self.fetch("users", "user_bg_id")

    @bg_id.setter
    def bg_id(self, value):
        self.db.connect()
        self.db.change_bg(self.id, value)
        self.db.close()

    @property
    def gil(self):
        return self.fetch("users", "user_gil")
    
    @property
    def level(self):
        return self.fetch("users", "user_level")
    
    @property
    def xp(self):
        return self.fetch("users", "user_xp")
    
    @property
    def xp_to_next(self):
        return self.fetch("users", "user_xp_to_next")
    
    @property
    def materia(self):
        return self.fetch("users", "user_materia")
    
    @property
    def followed_twitter(self):
        return self.fetch("social", "followed_twitter")

    @followed_twitter.setter
    def followed_twitter(self, value):
        self.db.connect()
        self.db.update_column("social", "followed_twitter", True, user_id=self.id)
        self.db.close()

    @property
    def followed_facebook(self):
        return self.fetch("social", "followed_facebook")

    @property
    def is_patron(self):
        return self.fetch("social", "is_patron")
    
    @property
    def badges(self):
        self.db.connect()
        result = sorted([Badge(item["item_id"], item["item_equipped"]) for item in self.db.get_items(self.id)], key=lambda x: x.id)
        self.db.close()
        return result
    
    @property
    def backgrounds(self):
        self.db.connect()
        result = [Background(bg["bg_id"]) for bg in self.db.get_backgrounds(self.id)]
        self.db.close()
        return result

    def add_gil(self, value):
        self.db.connect()
        self.db.add_gil(self.id, value)
        self.db.close()

    def add_xp(self, value):
        self.db.connect()
        if self.db.add_xp(self.id, value):
            self.db.next_level(self.id)
            self.db.close()
            return True
        self.db.close()
        return False

    def add_badge(self, badge_id):
        self.db.connect()
        self.db.add_item(self.id, badge_id, item_equipped=False)
        self.db.close()

    def add_bg(self, bg_id):
        self.db.connect()
        self.db.add_bg(self.id, bg_id)
        self.db.close()

    def equip_badge(self, badge_id):
        self.db.connect()
        result = self.db.toggle_item(self.id, badge_id)
        self.db.close()
        return result

    def remove_badge(self, badge_id):
        self.db.connect()
        self.db.remove_item(self.id, badge_id)
        self.db.close()

    def fetch(self, table_name, column_name):
        self.db.connect()
        result = self.db.get_user(self.id)[table_name][column_name]
        self.db.close()
        return result

    def is_registered(self):
        """
        This method makes sure the user is registered
        in the database. Otherwise, the user will be registered
        to it, and returns True unless internal errors happen.
        """
        self.db.connect()
        result = self.db.get_user(self.id)
        if not result or len(result) < 3:
            # register the user
            self.db.new_user(self.id)
            return True
        else:
            return True
        self.db.close()
