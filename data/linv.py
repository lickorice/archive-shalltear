import json

database_directory = 'data/inventory.json'
data = ''

class LickInventory():
    def init(self):
        """This initializes the JSON database."""
        self.load_file()
        pass

    def save_file(self):
        """This saves to the JSON file."""
        global data
        with open(database_directory, 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    
    def load_file(self):
        """This loads the JSON file."""
        global data
        with open(database_directory, 'r') as infile:  
            data = json.load(infile)

    def check_user(self, userID):
        """Returns a Boolean value indicating if the user already exists in the database."""
        global data
        if userID in data["inventory"]:
            return True
        return False

    def check_item(self, itemID, userID):
        """Returns a Boolean value indicating if the item already exists in user's inventory."""
        global data
        if not self.check_user(userID):
            self.add_user(userID)
        if itemID in self.get_items(userID):
            return True
        return False

    def add_user(self, userID):
        """Adds a user to the database. Returns a Boolean value if successful."""
        global data
        if self.check_user(userID):
            return False
        data["inventory"][userID] = []
        self.save_file()
        return True

    def add_item(self, userID, itemID):
        """Gives a user an item. Returns a Boolean value if successful."""
        global data
        if self.check_item(itemID, userID):
            return False
        data["inventory"][userID].append(itemID)
        self.save_file()
        return True

    def get_items(self, userID):
        """Returns a [list] of items given a user."""
        global data
        if not self.check_user(userID):
            self.add_user(userID)
        return data["inventory"][userID]

    def rm_item(self, userID, itemID):
        """Removes an item from a user's inventory"""
        global data
        if not self.check_user(userID):
            self.add_user(userID)
        if itemID in data["inventory"][userID]:
            data["inventory"][userID].remove(itemID)
            return True
        else:
            return False

    def equip_badge(self, userID, itemID):
        """Equips a badge, given the user and the badge."""
        global data
        if not self.check_user(userID):
            self.add_user(userID)
        if itemID in data["inventory"][userID]:
            _index = data["inventory"][userID].index(itemID)
            i = False
            if data["inventory"][userID][_index][1] == True:
                data["inventory"][userID][_index][1] = False
            else:
                data["inventory"][userID][_index][1] = True
                i = True
            self.save_file()
            return True, i
        else:
            return False, False
