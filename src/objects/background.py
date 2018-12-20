import json

class Background: # TODO: Can we generalize this? So it can be used throughout the program
    """
    Instantiates a Background object given an ID, and given that
    it exists in the JSON file.
    
    Args:
        bg_id (int): The ID of the background.

    Attributes:
        id (int): The ID of the background.
        name (str): The name of the background.
        price (int): The gil needed to purchase the background.
        price_tag (str): The price "tag" on display.
        img_url (str): The filename of the background image.
        is_exclusive (bool): If the background is exclusive to IPM.
    """
    # TODO: Update documentation for both bg and badges
    def __init__(self, bg_id):
        with open('assets/obj_bgs.json') as f:
            bg_shop = json.load(f)
        self.id = int(bg_id)
        bg_id = str(bg_id)
        self.img_url = bg_shop[bg_id]["img_url"]
        self.is_for_sale = True
        self.is_exclusive = bg_shop[bg_id]["is_exclusive"]
        self.price = bg_shop[bg_id]["price"]
        self.price_tag = bg_shop[bg_id]["price_tag"]
        self.name = bg_shop[bg_id]["name"]

    def __repr__(self):
        return f"Background({self.id})"