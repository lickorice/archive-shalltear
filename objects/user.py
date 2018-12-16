from data import db_users
from objects.background import Background
from objects.badge import Badge

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
        if self.is_registered():
            self.set_attr()

    @property
    def bg_id(self):
        return self.fetch("users", "bg_id")

    @bg_id.setter
    def bg_id(self, value):
        self.db.connect()
        self.db.change_bg(self.id, value)
        self.db.close()
    
    @property
    def gil(self):
        return self.fetch("users", "user_gil")

    @property
    def followed_twitter(self):
        return self.fetch("social", "followed_twitter")

    @property
    def badges(self):
        self.db.connect()
        result = Badge(item["item_id"], item["is_equipped"]) for item in self.db.get_items(self.id)]
        self.db.close()
        return result

    @property
    def backgrounds(self):
        self.db.connect()
        result = Background(bg["bg_id"]) for bg in self.db.get_backgrounds(self.id)]
        self.db.close()
        return result

    def add_gil(self, value):
        self.db.connect()
        self.db.add_gil(self.id, value)
        self.db.close()

    def add_badge(self, badge_id):
        self.db.connect()
        self.db.add_item(self.id, badge_id, item_equipped=False)
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

    def set_attr(self):
        x = self.db.get_user(self.id)
        profile, activities, social = x["users"], x["activities"], x["social"]

        self.level = profile["user_level"]
        self.xp = profile["user_xp"]
        self.xp_to_next = profile["user_xp_to_next"]
        self.materia = profile["user_materia"]
        
        self.followed_facebook = social["followed_facebook"]
        self.is_patron = social["is_patron"]

        # TODO: Add gacha