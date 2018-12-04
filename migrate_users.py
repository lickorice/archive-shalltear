import json
from data import db_helper, db_users

in_db = db_helper.DBHelper('data/.db')
in_db.connect()
with open('data/inventory.json') as f:
    inv = json.load(f)["inventory"]
user_db = db_users.UserHelper()
user_db.connect()
for row in in_db.fetch_rows("primary_db", False, userID="%"):
    user_id = int(row["userID"])
    user_level = int(row["level"])
    user_xp = int(row["experience"])
    user_xp_to_next = int(row["targetExp"])
    raw_gil = int(row["cash"])
    user_gil = int(raw_gil**(1/2))*5
    user_materia = (raw_gil-user_gil) * 5
    # print(user_id, user_level, user_xp, user_xp_to_next, raw_gil, user_gil, user_materia)
    user_db.new_user(user_id, user_level, user_xp, user_xp_to_next, user_gil, user_materia)
    try:
        for item in inv[row["userID"]]:
            item_id, item_equipped = item
            # print(user_id, int(item_id), item_equipped)
            user_db.add_item(user_id, int(item_id), item_equipped)
    except KeyError:
        pass
    user_items = user_db.get_items(user_id)
    user_items = list(set(list(map(lambda x: (x["item_id"], x["item_equipped"]), user_items))))
    # print(user_items)
    for item in user_items:
        user_db.remove_item(user_id, item[0])
        user_db.add_item(user_id, item[0], bool(item[1]))

user_db.close()
in_db.close()