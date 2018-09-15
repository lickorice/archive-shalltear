import sqlite3

database_directory = 'data/.db'
baseExperience, factor = 50, 1.5

db = sqlite3.connect(database_directory)


class LickDB():
    def init(self):
        """This initializes the database."""
        c = db.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS primary_db(
                        id INTEGER PRIMARY KEY,
                        userID TEXT UNIQUE,
                        cash INTEGER,
                        level INTEGER,
                        experience INTEGER,
                        targetExp INTEGER)
        """)
        db.commit()
        c.execute("""
        CREATE TABLE IF NOT EXISTS weights_db(
                        id INTEGER PRIMARY KEY,
                        chnID TEXT UNIQUE,
                        xpINC INTEGER)
        """)
        db.commit()

    def insertUser(self, userID):
        """This inserts a user into the database."""
        print("Inserting user [{}] to the database...".format(userID))
        c = db.cursor()
        c.execute('''INSERT INTO primary_db(userID, cash, level, experience, targetExp)
                    VALUES(?, 0, 1, 0, ?)''', (userID, baseExperience,))
        db.commit()

    def insertChannel(self, chnID, xpINC):
        """This inserts a channel into the database."""
        print("Inserting channel [{}] to the database...".format(chnID))
        c = db.cursor()
        c.execute('''INSERT INTO weights_db(chnID, xpINC)
                    VALUES(?, ?)''', (chnID, xpINC,))
        db.commit()

    def getCash(self, userID):
        """This returns a user's cash."""
        c = db.cursor()
        c.execute('''SELECT cash FROM primary_db WHERE userID =?''',
                  (userID,))
        cash = c.fetchone()
        return cash[0]

    def getExp(self, userID):
        """This returns a user's experience."""
        c = db.cursor()
        c.execute('''SELECT experience FROM primary_db WHERE userID =?''',
                  (userID,))
        experience = c.fetchone()
        return experience[0]

    def getLvl(self, userID):
        """This returns a user's level."""
        c = db.cursor()
        c.execute('''SELECT level FROM primary_db WHERE userID =?''',
                  (userID,))
        level = c.fetchone()
        return level[0]

    def getTarg(self, userID):
        """This returns a user's target experience."""
        c = db.cursor()
        c.execute('''SELECT targetExp FROM primary_db WHERE userID =?''',
                  (userID,))
        tExp = c.fetchone()
        return tExp[0]

    def getWeight(self, chnID):
        """This returns a channel's experience incrementation."""
        c = db.cursor()
        c.execute('''SELECT xpINC FROM weights_db WHERE chnID =?''',
                  (chnID,))
        xExp = c.fetchone()
        return xExp[0]

    def updateExp(self, userID, xp=2):
        # updates cash number of user
        curXP = self.getExp(userID)
        newXP = curXP + xp
        c = db.cursor()
        c.execute('''UPDATE primary_db SET experience = ? WHERE userID = ?''',
                  (newXP, userID))
        db.commit()
        return newXP

    def updateLvl(self, userID, residual=0):
        # updates cash number of user
        curLvl = self.getLvl(userID)
        newLvl = curLvl + 1
        newTarg = int(baseExperience * (newLvl ** factor))
        c = db.cursor()
        c.execute('''UPDATE primary_db SET level = ? WHERE userID = ?''',
                  (newLvl, userID))
        db.commit()
        c.execute('''UPDATE primary_db SET targetExp = ? WHERE userID = ?''',
                  (newTarg, userID))
        db.commit()
        c.execute('''UPDATE primary_db SET experience = ? WHERE userID = ?''',
                  (residual, userID))
        db.commit()
        return newLvl

    def updateCash(self, userID, cash):
        # updates cash number of user
        curCash = self.getCash(userID)
        newCash = curCash + cash
        c = db.cursor()
        c.execute('''UPDATE primary_db SET cash = ? WHERE userID = ?''',
                  (newCash, userID))
        db.commit()
        return newCash

    def updateWeight(self, chnID, weight):
        # updates cash number of user
        c = db.cursor()
        c.execute('''UPDATE weights_db SET xpINC = ? WHERE chnID = ?''',
                  (weight, chnID))
        db.commit()
