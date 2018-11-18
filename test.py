from data import gachadb
import random
import datetime

db = gachadb.GachaDB()

db.init()

prob_setting = {
    1: 20,
    2: 15,
    3: 7,
    4: 2,
    5: 1
}

all_cards = db.fetch_all_cards()

def roll():
    card_total = 0
    card_index = []
    for card in all_cards:
        card_total += prob_setting[card["RATING"]]
        card_index.extend([card["ID"] for i in range(prob_setting[card["RATING"]])])
    
    card_results = []

    for i in range(3):
        index = random.randrange(card_total)
        card_id = card_index[index]
        card_results.append(db.fetch_card(card_id))
        insert_card(card_id)

    # print(card_results)


def get_inventory():
    all_cards = db.get_all_cards(1)
    print(all_cards)


def insert_card(index):
    db.insert_card(1, index)


print(datetime.datetime.now().hour)