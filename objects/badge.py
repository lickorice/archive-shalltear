import json

class Badge:
    """
    Instantiates a Badge object given an ID, and given that
    it exists in the JSON file.
    
    Args:
        item_id (int): The ID of the badge.

    Attributes:
        id (int): The ID of the badge.
        name (str): The name of the badge.
        description (str): The badge's description
        price (int): The gil needed to purchase the badge.
        level_needed (int): The level needed to purchase the badge.
        price_tag (str): The price "tag" on display.
        icon_url (str): The filename of the badge's icon.
        is_exclusive (bool): If the badge is exclusive to IPM.
    """
    def __init__(self, item_id, is_equipped=False):
        with open('assets/obj_badgeshop.json') as f:
            badge_shop = json.load(f)
        with open('assets/obj_badges.json') as f:
            badge_json = json.load(f)
        self.id = int(item_id)
        item_id = str(item_id)
        self.is_equipped = is_equipped
        
        self.name = badge_json[item_id]["name"]
        if badge_json[item_id]["for_sale"]:
            self.is_exclusive = badge_shop[item_id]["is_exclusive"]
            self.price = badge_shop[item_id]["price"]
            self.price_tag = badge_shop[item_id]["price_tag"]
            self.level_needed = badge_shop[item_id]["level_needed"]
            self.icon_url = badge_shop[item_id]["icon_url"]
            self.description = badge_shop[item_id]["description"]
        else:
            self.icon_url = badge_json[item_id]["img-url"]
            self.description = badge_json[item_id]["description"]

    def __repr__(self):
        return f"Badge({self.id})"