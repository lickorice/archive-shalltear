# Bot details
CURRENT_VERSION = "1.1.0a"

ASSETS_DIRECTORY = "./assets/"
DATABASE_PATH = "./data/db/"

# Set for Lickorice, (Carlos Panganiban) and for IPM Collective server.
OWNER_ID = 319285994253975553
OWNER_GUILD_ID = 378540712653750274
OWNER_GUILD_INVITE = "https://discord.gg/XmC7fht" # #rules-info
BOT_INVITE_LINK = "https://discordapp.com/oauth2/authorize?client_id=490453816978702336&scope=bot&permissions=1580592192"
MY_PAYPAL = "https://paypal.me/lickorice"
MY_PATREON = "https://www.patreon.com/lickorice"
# OWNER_GUILD_ID = 442676019774750731 # uncomment for development

# Some set images:
DONATE_IMG = "" # TODO: add donation details

# Some important constants:
CLR_MAIN_COLOR = 0xff1155

# Set for IPM Collective server:
VIP_ROLE_ID = 444142897290412053
VIP_CHANNEL_ID = 444150135664934912

# Set defaults for profile image generation
DIR_LEVELUP = "temp/levelup.png"
DIR_PROFILE = "temp/profile.png"
DIR_MEME = "temp/meme_temp.png"

# Set emojis for paginated embeds:
EMJ_LEFT_PAGE = "◀"
EMJ_RIGHT_PAGE = "▶"

# Messages below, please arrange alphabetically:
# Lick: People who set messages not in alphabetical order will be stoned.
MSG_ABOUT_TITLE = "About Shalltear"
MSG_AM_I_A_JOKE = "**<@{}>, am I a joke to you?** https://cdn.discordapp.com/attachments/443734016257163264/519524509020061736/joke.png"
MSG_AUTHOR_INFO = "Carlos Panganiban | github.com/lickorice | cgpanganiban@up.edu.ph | @cgpanganiban"
MSG_AUTHOR_NAME = "Lickorice#5638"
MSG_BADGE_ALREADY_EXISTS = "**You already have that badge.**"
MSG_BADGE_ALREADY_EXISTS_2 = "**User already has that badge.**"
MSG_BADGE_ALREADY_YOURS = "<@{}>, you already have that badge. See your equipped badges with `s!badges` and equip them with `s!equip`."
MSG_BADGE_BOUGHT = "<@{}>, you have successfully bought **{}**!."
MSG_BADGE_EQUIPPED = "**{}** successfully equipped."
MSG_BADGE_FULL = "<@{}>, you have equipped the maximum number of badges (11), please unequip some badges before equipping a new one."
MSG_BADGE_GRANT_FAILURE = "**User already has that badge.**"
MSG_BADGE_GRANT_SUCCESS = "**Badge successfully granted.**"
MSG_BADGE_NONE = "**{}**, you have no badges yet."
MSG_BADGE_NOT_FOUND = "**That badge doesn't exist.**"
MSG_BADGE_NOT_YOURS = "<@{}>, you don't have that badge."
MSG_BADGE_RECEIVED = "<@{}>, you have received the **{}** badge!"
MSG_BADGE_UNEQUIPPED = "**{}** successfully unequipped."
MSG_BALANCE = "<@{}>, you currently have **{} 💰** Gil."
MSG_BG_ALREADY_YOURS = "<@{}>, you already have that background. Change into it with `s!changebg`."
MSG_BG_BOUGHT = "<@{}>, you have successfully bought **{}** for **{} 💰** gil!"
MSG_BG_CHANGED = "**{}**, you have successfully changed your background to **{}**."
MSG_BG_NOT_FOUND = "**That background doesn't exist.**"
MSG_BG_NOT_YOURS = "**{}**, you don't own that background. Browse the shop with `s!bgshop` to view our collection of profile backgrounds!"
MSG_BG_PREVIEW = "Previewing **{}**"
MSG_BG_RESET = "**All user backgrounds successfully reset to default.**"
MSG_BLOCKED = "<@{}>, it seems that you may have **blocked** me! Kindly unblock me so I could send you *secret messages!* :wink:"
MSG_BOT_DONATE = f"**Donate to the developer and get amazing rewards!** Details here: {DONATE_IMG} \n**Patreon:** {MY_PATREON}\n**PayPal:** {MY_PAYPAL}"
MSG_BOT_INVITE = "**Get Shalltear to join your server!** Use this link: {}"
MSG_CMD_ERROR = "<@{}>, **try again.** *({})*"
MSG_CMD_NODMS = "**You can't use that command in private messages.**"
MSG_CMD_NOT_FOUND = "<@{}>, **that command does not exist.**"
MSG_DM_SENT = "**{}, DM sent!**"
MSG_EXCLUSIVE_SERVER = "**Join my exclusive server at IPM Collective!** Get access to countless backgrounds, gacha items, badges, and more at {} !"
MSG_GACHA_CARD_DNE = "**{}**, that card does not exist."
MSG_GACHA_STREAK = "**{}**, here's the results of your booster pack!\nYour current streak: **{}**\nCheck back after an hour to advance your streak and claim more cards! (Streaks reset after 12)"
MSG_GACHA_FUNDS_DEDUCT = "**{}**, **{}** gil have been deducted from your account."
MSG_GACHA_INSUF_FUNDS = "**{}**, you do not have enough Materia to afford a booster pack. A pack costs **{}** Gil."
MSG_GACHA_SERIES_DNE = "**{}**, that series does not exist."
MSG_GIL_CHECK = "**{}**, you currently have **{}** 💰 gil."
MSG_GIL_CHECK2 = "**{}** currently has **{}** 💰 gil."
MSG_GIL_RECEIVED = "<@{}>, you have received **{}** 💰 gil by {}."
MSG_GIVE = "<@{}>, you have received **{} 💰** from <@{}>"
MSG_GIVE_NO_USER = "<@{}>, please specify a user and try again."
MSG_GRANT_ALL_NEGATIVE = "A gilded, platinum blade falls from the sky and strikes the earth! **{} 💰** is removed from everyone's account. *(You may also be in debt.)*"
MSG_GRANT_ALL_POSITIVE = "The cloudy sky clears out within an instant and brings forth a godly, blinding light! It rains Gil! **Everyone gains {} 💰!**"
MSG_GRANT_ERROR = "**Please enter a gil value other than 0.**"
MSG_GRANT_NEGATIVE = "A booming voice echoes within your mind, <@{}>! It demands your Gil and therefore magically disintegrated **{} 💰** from your account. *(You may also be in debt.)*"
MSG_GRANT_POSITIVE = "A golden ray of light pierces the sky and onto the earth, materializing Gil upon the spot where <@{}> stands. The great gods from above have given divine mercy and has given him **{} 💰!**"
MSG_INSUF_FUNDS = "**<@{}>, insufficient funds.**"
MSG_INSUF_GIL = "**Insufficient gil.** You can earn 500 gil by following the developer through `s!twitter`!"
MSG_INSUF_LVL = "**Level too low.**"
MSG_INSUF_PERMS = "**Insufficient permissions.**"
MSG_INVALID_AMOUNT = "**<@{}>, you entered an invalid amount.**"
MSG_INVALID_CMD = "**Invalid command parameters.**"
MSG_ITEM_IS_EXCLUSIVE = "**That item is exclusive only to the IPM Collective.** If you wish to purchase the item, join the exclusive item by doing `s!exclusive`."
MSG_ITEM_NOT_FOUND = "**No such item found.**"
MSG_ITEM_NOT_FOR_SALE = "**That item is not for sale.**"
MSG_LOGGING_OUT = "**Logging out...**"
MSG_SET_PREMIUM1 = "Successfully set **{}** as a premium user."
MSG_SET_PREMIUM2 = "Successfully set **{}** as a non-premium user."
MSG_SWEEPSTAKES_LOSS = "**{}**, sadly, you lost."
MSG_SWEEPSTAKES_NO = "**{}**, please enter a number from 0-999."
MSG_SWEEPSTAKES_POT = "The current jackpot for the lottery is **{} 💰** gil."
MSG_SWEEPSTAKES_WIN = "<@{}>, **congratulations!** You won the jackpot of **{} 💰** gil!."
MSG_MATERIA_CHECK = "**{}**, you currently have **{}** 💎 materia."
MSG_MATERIA_CHECK2 = "**{}** currently has **{}** 💎 materia."
MSG_MEME_NOT_ENOUGH = "**Not enough actors!** You need {} actor{} for this meme to be generated."
MSG_MEME_NOT_FOUND = "**Meme not found!**"
MSG_NEET_ROLE_NAME_WAIT = "<@{}>, please reply with the **custom role name** you want for you!\nThe name could only be **32 characters long**, and please refrain from using any profanity in the name."
MSG_NEET_ROLE_CONFIRM = "<@{}>, **{}** is your chosen role name. Is this correct? (Reply with Y/N)"
MSG_NEET_ROLE_CREATE = "<@{}>, you have been assigned **{}**! Have fun!"
MSG_ON_COOLDOWN = "**{}**, free booster packs are only claimable once per hour. The next interval you can claim one will be in **{}** minute{}."
MSG_PING = "Pong! (**{}**ms)"
MSG_PROFILE_BG_RESET = "**All profile backgrounds successfully reset.**"
MSG_REGISTER_1 = "**Attempting to register users...**"
MSG_REGISTER_2 = "**Attempting to register users...\n({}/{})**"
MSG_REGISTER_3 = "**{0}** of **{1}** users successfully registered.\nOut of all **{1}** users, **{2}** are bots."
MSG_REWARDS_1 = "**{}**, you can only receive these rewards only once per lifetime!"
MSG_REWARDS_2 = "**{}**, that account is already used to redeem rewards!"
MSG_ROLE_ASSIGNED = "**{}**, you have successfully assigned yourself **{}**."
MSG_ROLE_DNE = "**That role does not exist.** Make sure you spelled the role name correctly."
MSG_ROLE_NONE = "**There are no self-assignable roles for this server.**"
MSG_ROLE_NOT_ASSIGNABLE = "<@{}>, that role is **not self-assignable**. Contact your server moderator/administrator if you wish for this role to be self-assignable."
MSG_ROLE_TOGGLE_1 = "**{}** successfully set as self-assignable."
MSG_ROLE_TOGGLE_2 = "**{}** successfully removed as self-assignable."
MSG_ROLE_TOGGLE_3 = "**{}** is a higher role than my top role, please elevate my role before setting this as self-assignable."
MSG_ROLE_UNASSIGNED = "**{}**, you have successfully removed **{}**."
MSG_SRC_LINK = "http://bit.ly/shalltearBOT"
MSG_TIMEOUT = "<@{}>, **you timed out.**"
MSG_TWITTER_AUTH = "**{}**, authorize me in order to follow! {}\nSimply send a message with the **authentication PIN,** then, I will automatically follow https://twitter.com/cgpanganiban for you!\n(This will time out after five minutes)"
MSG_USER_NOT_FOUND = "**No such user found.**"
MSG_VIP_WELCOME = "<@{}>, welcome to the VIP channels! Please take note of the following rules: ```1. No screenshots of this channel are allowed.\n2. Everything that you say and hear, stays here.```*** Enjoy your stay in VIP!***"