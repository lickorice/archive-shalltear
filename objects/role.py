from data import db_roles
class Assignable:
    """
    Self-defined Assignable object containing most of Shalltear-
    essential attributes and methods.

    Args:
        role_id (int): The role's ID.
        guild_id (int): The guild's ID.

    Attributes:
        id (int): The role's ID.
        guild (int): The guild's ID.
        db (data.db_roles.RoleHelper): The current RoleHelper instance
            to help with database operations.
    """
    
    def __init__(self, role_id, guild_id, tag=False):
        self.id = role_id
        self.guild = guild_id
        self.tag = tag
        self.db = db_roles.RoleHelper(False)
        # Checking if the role exists:
        self.db.connect()
        
        try:
            self.hash = self.db.get_role(self.guild, self.id)
        except IndexError:
            self.hash = False

        self.db.close()

    def __repr__(self):
        return "Assignable({}, {}, {})".format(
            self.id, self.guild, self.tag
        )

    def toggle_assignable(self):
        self.db.connect()
        result = self.db.new_assignable(self.guild, self.id, self.tag)
        if not result:
            self.db.remove_role(self.guild, self.id)
        self.db.close()
        return result

    def change_tag(self, tag):
        return self.db.change_tag(self.guild, self.id, tag)
        