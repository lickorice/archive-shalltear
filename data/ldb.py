import sqlite3

database_directory = 'data/.db'
baseExperience, factor = 50, 1.1

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

    def insertUser(self, userID):
        """This inserts a user into the database."""
        print("Inserting user [{}] to the database...".format(userID))
        c = db.cursor()
        c.execute('''INSERT INTO primary_db(userID, cash, level, experience, targetExp)
                    VALUES(?, 0, 1, 0, ?)''', (userID, baseExperience,))
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
