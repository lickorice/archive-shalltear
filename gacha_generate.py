from data import gachadb
import random, sqlite3

db = gachadb.GachaDB()

db.init()
wifecount = 0

while True:
    name = input()
    if name == 'END':
        print("Successfully registered {} wives.".format(wifecount))
        break
    img_url = input()
    card_type = int(input())
    rating = int(input())
    series_id = int(input())
    try:
        db.register_card(name, img_url, rating, card_type, series_id)
        wifecount += 1
    except sqlite3.IntegrityError:
        pass