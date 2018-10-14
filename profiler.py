

from PIL import Image, ImageFont, ImageDraw
import requests, json
from io import BytesIO

with open('assets/str_titles.json') as f:
    str_titles = json.load(f)

def generate(user_name, avatar_url, user_level, user_xp):
    """
    This is a profile image generator, dev'd by Carlos Panganiban. 2018.
    It takes in the following arguments:
    generate(
        user_name= (str) The user's name;
        avatar_url= (str) The user's avatar URL;
        user_level= (int) The user's level;
        user_xp = (int, int) The user's current, and next level xp
    )
    """

    if user_level >= 30:
        user_title = "The Conqueror of Servers"
    else:
        user_title = str_titles[str(user_level)]
    template = Image.open('assets/img_profile-template.png')
    
    avatar_file = requests.get(avatar_url)
    avatar = Image.open(BytesIO(avatar_file.content))
    avatar = avatar.resize((90, 90), Image.BILINEAR)
    template.paste(avatar, (20, 30))

    fillcolor, strokecolor, strokecolor_2, name_size = "white", "black", (100, 100, 100, 255), 50
    font_username = ImageFont.truetype('assets/ttf_rob-username.ttf', name_size)
    font_title = ImageFont.truetype('assets/ttf_title.ttf', 20)
    draw = ImageDraw.Draw(template)
    _x, _y = 130, 20

    while True:
        if draw.textsize(user_name, font_username)[0] <= 355:
            break
        else:
            _y += 5
            name_size -= 5
            font_username = ImageFont.truetype('assets/ttf_rob-username.ttf', name_size)

    draw.text((_x+1, _y), user_name, font=font_username, fill=strokecolor)
    draw.text((_x-1, _y), user_name, font=font_username, fill=strokecolor)
    draw.text((_x, _y-1), user_name, font=font_username, fill=strokecolor)
    draw.text((_x, _y+1), user_name, font=font_username, fill=strokecolor)
    draw.text((_x+1, _y+1), user_name, font=font_username, fill=strokecolor)
    draw.text((_x-1, _y-1), user_name, font=font_username, fill=strokecolor)
    draw.text((_x+1, _y-1), user_name, font=font_username, fill=strokecolor)
    draw.text((_x-1, _y+1), user_name, font=font_username, fill=strokecolor)

    draw.text((_x, _y), user_name, font=font_username, fill=fillcolor)
    _x, _y = 130, 80
    draw.text((_x, _y), user_title, font=font_title, fill=strokecolor)
    _x, _y = 130, 100
    draw.text((_x, _y), "LEVEL {}".format(user_level), font=font_title, fill=strokecolor_2)
    _x, _y = 190, 109
    lvl_temp = Image.new('RGBA', (295, 4), (44, 47, 51, 255))
    lvl_temp_2 = Image.new('RGBA', ((295 * user_xp[0]) // user_xp[1], 4), (255, 17, 85, 255))
    template.paste(lvl_temp, (_x, _y))
    template.paste(lvl_temp_2, (_x, _y))

    
    template.save('temp/profile.png')


def main():
    generate("Lickorice#6969", 'https://cdn.discordapp.com/avatars/319285994253975553/bafd915352039cbfaf66a40a9a2210c7.png', 50, (75, 100))

if __name__ == '__main__':
    main()