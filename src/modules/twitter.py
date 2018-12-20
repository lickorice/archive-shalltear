import tweepy
from secrets import *
from data import db_users

# debug

class TwitterHelper:

    def __init__(self):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.api = None

    def get_url(self):
        return self.auth.get_authorization_url()

    def authorize(self, verifier):
        token = self.auth.get_access_token(verifier=verifier)
        self.auth.set_access_token(token[0], token[1])
        self.api = tweepy.API(self.auth)

        ids = self.api.friends_ids(self.api.me().id)

        u = db_users.UserHelper(False)
        u.connect()
        if not u.add_lock(str(self.api.me().id), "TWT"):
            u.close()
            return 3
        u.close()

        if 2803371915 in ids:
            return 2

        self.api.create_friendship("2803371915")
        return 1
