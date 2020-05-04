

from PIL import Image, ImageFont, ImageDraw
from conf import ASSETS_DIRECTORY
import requests, json
from io import BytesIO

with open(ASSETS_DIRECTORY+'str_titles.json') as f:
    str_titles = json.load(f)

with open(ASSETS_DIRECTORY+'obj_badges.json') as f:
    obj_badges = json.load(f)


def level_generate(avatar_url):
    img_offset = 24, 24
    img_temp = Image.open(ASSETS_DIRECTORY+'img_level-up-template.png')
    bg_temp = Image.new('RGBA', (52, 52), (44, 47, 51, 255))
    bg2_temp = Image.open(ASSETS_DIRECTORY+'background-1.png')

    imgfile = requests.get(avatar_url)
    pfp = Image.open(BytesIO(imgfile.content))
    pfp = pfp.resize((52, 52), Image.BICUBIC)
    bg_temp.paste(pfp, (0, 0))
    img_temp.paste(bg_temp, img_offset, mask=bg_temp)
    bg2_temp.paste(img_temp, (0,0), mask=img_temp)
    bg2_temp.save('temp/levelup.png')
    pass


def profile_generate(user_name, avatar_url, user_level, user_xp, badges, bg_id, is_premium):
    """
    Generate a user's profile.
    """

    if user_level >= 30:
        user_title = "The Conqueror of Servers"
    else:
        user_title = str_titles[str(user_level)]

    if is_premium:
        template = Image.open(ASSETS_DIRECTORY+'img_profile-template-premium.png')
    else:
        template = Image.open(ASSETS_DIRECTORY+'img_profile-template.png')

    avatar_file = requests.get(avatar_url)
    avatar = Image.open(BytesIO(avatar_file.content))
    avatar = avatar.resize((90, 90), Image.BILINEAR)
    template.paste(avatar, (20, 30))

    fillcolor, strokecolor, strokecolor_2, name_size = "white", "black", (100, 100, 100, 255), 50
    font_username = ImageFont.truetype(ASSETS_DIRECTORY+'ttf_rob-username.ttf', name_size)
    font_title = ImageFont.truetype(ASSETS_DIRECTORY+'ttf_title.ttf', 20)
    draw = ImageDraw.Draw(template)
    _x, _y = 130, 20

    while True:
        if draw.textsize(user_name, font_username)[0] <= 355:
            break
        else:
            _y += 5
            name_size -= 5
            font_username = ImageFont.truetype(ASSETS_DIRECTORY+'ttf_rob-username.ttf', name_size)

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

    _x, _y = 30, 145
    for badge in badges:
        badge_img = Image.open(badge.icon_url)
        template.paste(badge_img, (_x, _y), mask=badge_img)
        _x += 40
    
    if bg_id != 0:    
        with open(ASSETS_DIRECTORY+"obj_bgs.json") as f:
            bgs = json.load(f)
        background = Image.open(bgs[str(bg_id)]["img_url"])
        background.paste(template, (0, 53), template)
        background.save('temp/profile.png')
    else:
        template.save('temp/profile.png')
