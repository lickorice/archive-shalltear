from data import db_helper

# Level config
base_exp, factor = 50, 1.5

class UserHelper(db_helper.DBHelper):
    def __init__(self):
        self.database_path = 'data/db/user.db'

    def new_user(self, user_id):
        self.insert_row(
            table_name="users",
            user_id=user_id,
            user_level=1,
            user_xp=0,
            user_xp_to_next=50,
            user_gil=0,
            user_materia=0,
            user_bg_id=0
            )
        self.insert_row(
            table_name="activities",
            user_id=user_id,
            can_free_pack=True,
            can_daily=True,
            count_free_gil=0,
            count_commands=0,
            count_rolls=0,
            count_cards=0
            )

    def get_user(self, user_id):
        x = {
            "users": self.fetch_rows("users", user_id=user_id)[0],
            "activities": self.fetch_rows("activities", user_id=user_id)[0]
            }
        return x

    def add_gil(self, user_id, value):
        self.increment_value(user_id, "users", "user_gil", value)

    def add_materia(self, user_id, value):
        self.increment_value(user_id, "users", "user_materia", value)

    def add_item(self, user_id, item_id):
        self.insert_row(
            table_name="inventory",
            owner_id=user_id,
            item_id=item_id,
            item_equipped=False
        )
    
    def change_bg(self, user_id, bg_id):
        self.update_column("users", "user_bg_id", bg_id, user_id=user_id)

    def next_level(self, user_id):
        current_user = self.get_user(user_id)["users"]
        new_next = int(base_exp * ((current_user["user_level"]+1) ** factor))
        self.increment_value(user_id, "users", "user_level", 1)
        self.update_column("users", "user_xp", 0, user_id=user_id)
        self.update_column("users", "user_xp_to_next", new_next, user_id=user_id)

    def increment_value(self, user_id, table_name, column, value):
        # Utility function. Don't call directly.
        first_value = self.get_user(user_id)[table_name][column]
        self.update_column(table_name, column, (first_value+value), user_id=user_id)


def main():
    test = UserHelper("db/user.db")
    test.connect()
    test.new_user(11)
    print(test.get_user(11)["users"])
    test.change_bg(11, 2)
    print(test.get_user(11)["users"])


if __name__ == '__main__':
    main()