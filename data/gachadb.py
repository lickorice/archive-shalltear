import sqlite3

database_directory = 'data/gacha.db'
baseExperience, factor = 50, 1.5

db = sqlite3.connect(database_directory)


class GachaDB():
    def init(self):
        """This initializes the database."""
        c = db.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS inventory_db(
                        id INTEGER PRIMARY KEY,
                        userID TEXT,
                        cardID INTEGER)
        """)
        db.commit()
        c.execute("""
        CREATE TABLE IF NOT EXISTS cards_db(
                        id INTEGER PRIMARY KEY,
                        card_type INTEGER,
                        name TEXT UNIQUE,
                        imgURL TEXT UNIQUE,
                        rating INTEGER,
                        seriesID INTEGER)
        """)
        db.commit()
        c.execute("""
        CREATE TABLE IF NOT EXISTS cooldown_db(
                        id INTEGER PRIMARY KEY,
                        userID TEXT UNIQUE)
        """)
        db.commit()

    def insert_card(self, userID, cardID):
        """This inserts an ownership into the database."""
        c = db.cursor()
        c.execute('''INSERT INTO inventory_db(userID, cardID)
                    VALUES(?, ?)''', (userID, cardID,))
        db.commit()

    def get_all_cards(self, userID):
        """This returns all of a user's cards."""
        c = db.cursor()
        c.execute('''SELECT cardID FROM inventory_db WHERE userID =?''',
                  (userID,))
        cards = c.fetchall()
        return cards

    def remove_card(self, userID, cardID):
        """This removes a user's card."""
        c = db.cursor()
        c.execute('''DELETE FROM tasks WHERE userID=? AND cardID = ?''',
                  (userID, cardID))
        db.commit()

    def register_card(self, card_name, img_url, rating, card_type, series_id):
        """This inserts a card name into the database."""
        c = db.cursor()
        c.execute('''INSERT INTO cards_db(name, imgURL, rating, card_type, seriesID)
                    VALUES(?, ?, ?, ?, ?)''', (card_name, img_url, rating, card_type, series_id))
        db.commit()

    def fetch_card(self, target_card):
        """This returns a card's info."""

        target_card_int = -1
        try:
            target_card_int = int(target_card)
        except ValueError:
            pass

        c = db.cursor()
        c.execute('''SELECT * FROM cards_db WHERE id = ? OR name LIKE ?''',
                  (target_card_int, '{}%'.format(target_card)))
        card = c.fetchone()
        if card == None:
            return False
        card = self.cardify(card[2], card[3], card[4], card[1], card[0], card[5])
        return card

    def put_on_cooldown(self, userID):
        """This inserts a card name into the database."""
        c = db.cursor()
        try:
            c.execute('''INSERT INTO cooldown_db(userID)
                        VALUES(?)''', (userID,))
            db.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def clear_cooldown(self):
        """This clears all cooldowns."""
        c = db.cursor()
        c.execute('''DELETE FROM cooldown_db''')
        db.commit()

    def fetch_all_cards(self, seriesID=None):
        """Returns all cards."""
        c = db.cursor()
        if seriesID == None:
            c.execute("SELECT * FROM cards_db")
        else:
            c.execute("SELECT * FROM cards_db WHERE seriesID ?", (int(seriesID),))

        raw_cards = c.fetchall()
        cards = []
        for card in raw_cards:
            cards.append(self.cardify(card[2], card[3], card[4], card[1], card[0], card[5]))

        return cards

    def sell_card(self, userID, cardID):
        """Sells a card."""
        c = db.cursor()
        c.execute("SELECT * FROM inventory_db WHERE userID=? and cardID=?", (userID, cardID))

        raw_cards = c.fetchall()
        if len(raw_cards) == 0:
            return False
        else:
            c.execute('''DELETE FROM inventory_db WHERE id=?''', (raw_cards[0][0],))
            db.commit()
            return True


    def cardify(self, name, image, rating, card_type, card_id, series_id):
        """Makes a card object."""
        card = {}
        card["ID"] = card_id
        card["NAME"] = name
        card["IMG"] = image
        card["RATING"] = rating
        card["CARD_TYPE"] = card_type
        card["SERIES_ID"] = series_id
        return card