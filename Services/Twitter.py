import tweepy
from Hook import requires
from Configuration import ConfigFile

TwitConfig = ConfigFile("..", "Configs", "Twitter")

if not TwitConfig:
    raise Exception("No Twitter Configuration Found")

CONSUMER_KEY = TwitConfig['twitter', 'consumer_key']
CONSUMER_SECRET = TwitConfig['twitter', 'consumer_secret']
ACCESS_KEY = TwitConfig['twitter', 'access_key']
ACCESS_SECRET = TwitConfig['twitter', 'access_secret']


class Twitter:
    def postUpdate(self, update):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        status = api.update_status(update)
        if status: 
            return True

    def onEvent(self, event):
        event['postUpdate'] = self.postUpdate
