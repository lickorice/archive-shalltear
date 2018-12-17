
import sqlite3, hashlib
from data import db_helper
base_exp, factor = 50, 1.5

class RoleHelper(db_helper.DBHelper):
    def __init__(self, is_logged=True):
        self.database_path = 'data/db/misc.db'
        self.is_logged = is_logged

    def new_assignable(self, guild_id, role_id, tag="none"):
        """Adds a new assignable role to the database."""
        x = (str(guild_id)+str(role_id)).encode('utf-8')
        x = hashlib.sha1(x).hexdigest()
        try:
            self.insert_row(
                table_name="assignables",
                guild_id=guild_id,
                role_id=role_id,
                tag=tag,
                hash=x
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_roles(self, guild_id):
        """Fetches all self-assignables given a guild ID."""
        return self.fetch_rows("assignables", True, guild_id=guild_id)
    
    def get_role(self, guild_id, role_id):
        """Fetches a self-assignable given its IDs."""
        try:
            return self.fetch_rows("assignables", True, guild_id=guild_id, role_id=role_id)[0]
        except IndexError:
            return None

    def remove_role(self, guild_id, role_id):
        """Removes a self-assignable from the table."""
        self.remove_rows(
            table_name="assignables",
            guild_id=guild_id, role_id=role_id
        )

    def change_tag(self, guild_id, role_id, tag):
        """
        Changes the tag assigned to the self-assignable.
        Pass False to remove tag.
        """
        tag = tag if tag else "None"
        self.update_column(
            "assignables", "tag", tag, guild_id=guild_id, role_id=role_id
        )
