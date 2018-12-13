class Config():
    def __init__(self):
        # Set for Lickorice, (Carlos Panganiban) and for IPM Collective server.
        self.OWNER_ID = 319285994253975553
        self.OWNER_GUILD_ID = 378540712653750274
        # self.OWNER_GUILD_ID = 442676019774750731 # uncomment for development

        # Some important constants:
        self.CLR_MAIN_COLOR = 0xff1155

        # Set for IPM Collective server:
        self.VIP_ROLE_ID = 444142897290412053
        self.VIP_CHANNEL_ID = 444150135664934912

        # Set defaults for profile image generation
        self.DIR_LEVELUP = "temp/levelup.png"
        self.DIR_PROFILE = "temp/profile.png"

        # Set emojis for paginated embeds:
        self.EMJ_LEFT_PAGE = "◀"
        self.EMJ_RIGHT_PAGE = "▶"

        # Messages below, please arrange alphabetically:
        # Lick: People who set messages not in alphabetical order will be stoned.
        self.MSG_ABOUT_TITLE = "About Shalltear"
        self.MSG_AM_I_A_JOKE = "**<@{}>, am I a joke to you?** https://cdn.discordapp.com/attachments/443734016257163264/519524509020061736/joke.png"
        self.MSG_AUTHOR_INFO = "Carlos Panganiban | github.com/lickorice | cgpanganiban@up.edu.ph | @cgpanganiban"
        self.MSG_AUTHOR_NAME = "Lickorice#5638"
        self.MSG_BADGE_ALREADY_EXISTS = "**You already have that badge.**"
        self.MSG_BADGE_ALREADY_EXISTS_2 = "**User already has that badge.**"
        self.MSG_BADGE_ALREADY_YOURS = "<@{}>, you already have that badge. See your equipped badges with `s!badges` and equip them with `s!equip`."
        self.MSG_BADGE_BOUGHT = "<@{}>, you have successfully bought **{}**!."
        self.MSG_BADGE_EQUIPPED = "**{}** successfully equipped."
        self.MSG_BADGE_FULL = "<@{}>, you have equipped the maximum number of badges (11), please unequip some badges before equipping a new one."
        self.MSG_BADGE_GRANT_FAILURE = "**User already has that badge.**"
        self.MSG_BADGE_GRANT_SUCCESS = "**Badge successfully granted.**"
        self.MSG_BADGE_NONE = "You have no badges yet."
        self.MSG_BADGE_NOT_FOUND = "**That badge doesn't exist.**"
        self.MSG_BADGE_NOT_YOURS = "<@{}>, you don't have that badge."
        self.MSG_BADGE_UNEQUIPPED = "**{}** successfully unequipped."
        self.MSG_BALANCE = "<@{}>, you currently have **{} 💰** Gil."
        self.MSG_BG_ALREADY_YOURS = "<@{}>, you already have that background. Change into it with `s!changebg`."
        self.MSG_BG_BOUGHT = "<@{}>, you have successfully bought **{}** for **{} 💰** gil!"
        self.MSG_BG_CHANGED = "**{}**, you have successfully changed your background to **{}**."
        self.MSG_BG_NOT_FOUND = "**That background doesn't exist.**"
        self.MSG_BG_NOT_YOURS = "**{}**, you don't own that background. Browse the shop with `s!bgshop` to view our collection of profile backgrounds!"
        self.MSG_BG_PREVIEW = "Previewing **{}**"
        self.MSG_BG_RESET = "**All user backgrounds successfully reset to default.**"
        self.MSG_CMD_ERROR = "**<@{}>, try again.** *({})*"
        self.MSG_GACHA_CARD_DNE = "**{}**, that card does not exist."
        self.MSG_GACHA_FUNDS_DEDUCT = "**{}**, **{}** gil have been deducted from your account."
        self.MSG_GACHA_INSUF_FUNDS = "**{}**, you do not have enough Gil to afford a booster pack. A pack costs **{}** Gil."
        self.MSG_GACHA_NO_DUPE = "**{}**, you don't have any dupes to sell."
        self.MSG_GACHA_SELL_FAIL = "**{}**, you don't have that card."
        self.MSG_GACHA_SELL_SUCC = "**{}**, you have successfully sold **{}** for **{}** gil."
        self.MSG_GACHA_SERIES_DNE = "**{}**, that series does not exist."
        self.MSG_GACHA_YES_DUPE = "**{}**, you have sold **{}** dupe{} for **{}** gil."
        self.MSG_GIL_CHECK = "**{}**, you currently have **{}** 💰 gil."
        self.MSG_GIL_CHECK2 = "**{}** currently has **{}** 💰 gil."
        self.MSG_GIVE = "<@{}>, you have received **{} 💰** from <@{}>"
        self.MSG_GIVE_NO_USER = "<@{}>, please specify a user and try again."
        self.MSG_GRANT_ALL_NEGATIVE = "A gilded, platinum blade falls from the sky and strikes the earth! **{} 💰** is removed from everyone's account. *(You may also be in debt.)*"
        self.MSG_GRANT_ALL_POSITIVE = "The cloudy sky clears out within an instant and brings forth a godly, blinding light! It rains Gil! **Everyone gains {} 💰!**"
        self.MSG_GRANT_ERROR = "**Please enter a gil value other than 0.**"
        self.MSG_GRANT_NEGATIVE = "A booming voice echoes within your mind, <@{}>! It demands your Gil and therefore magically disintegrated **{} 💰** from your account. *(You may also be in debt.)*"
        self.MSG_GRANT_POSITIVE = "A golden ray of light pierces the sky and onto the earth, materializing Gil upon the spot where <@{}> stands. The great gods from above have given divine mercy and has given him **{} 💰!**"
        self.MSG_INSUF_FUNDS = "**<@{}>, insufficient funds.**"
        self.MSG_INSUF_GIL = "**Insufficient gil.**"
        self.MSG_INSUF_LVL = "**Level too low.**"
        self.MSG_INSUF_PERMS = "**Insufficient permissions.**"
        self.MSG_INVALID_AMOUNT = "**<@{}>, you entered an invalid amount.**"
        self.MSG_INVALID_CMD = "**Invalid command parameters.**"
        self.MSG_ITEM_NOT_FOUND = "**No such item found.**"
        self.MSG_LOGGING_OUT = "**Logging out...**"
        self.MSG_SWEEPSTAKES_LOSS = "**{}**, sadly, you lost."
        self.MSG_SWEEPSTAKES_NO = "**{}**, please enter a number from 0-999."
        self.MSG_SWEEPSTAKES_POT = "The current jackpot for the lottery is **{} 💰** gil."
        self.MSG_SWEEPSTAKES_WIN = "<@{}>, **congratulations!** You won the jackpot of **{} 💰** gil!."
        self.MSG_MEME_NOT_ENOUGH = "**Not enough actors!** You need {} actor{} for this meme to be generated."
        self.MSG_MEME_NOT_FOUND = "**Meme not found!**"
        self.MSG_ON_COOLDOWN = "**{}**, free booster packs are only claimable once per hour. The next interval you can claim one will be in **{}** minute{}."
        self.MSG_PING = "Pong! (**{}**ms)"
        self.MSG_REGISTER_1 = "**Attempting to register users...**"
        self.MSG_REGISTER_2 = "**Attempting to register users...\n({}/{})**"
        self.MSG_REGISTER_3 = "**{0}** of **{1}** users successfully registered.\nOut of all **{1}** users, **{2}** are bots."
        self.MSG_SRC_LINK = "http://bit.ly/shalltearBOT"
        self.MSG_TIMEOUT = "**<@{}>, you timed out.**"
        self.MSG_USER_NOT_FOUND = "**No such user found.**"
        self.MSG_VIP_WELCOME = "<@{}>, welcome to the VIP channels! Please take note of the following rules: ```1. No screenshots of this channel are allowed.\n2. Everything that you say and hear, stays here.```*** Enjoy your stay in VIP!***"