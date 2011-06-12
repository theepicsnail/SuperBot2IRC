from Hook import bindFunction, requires

@requires("Twitter", "IRCArgs")
class Twitter:
    @bindFunction(command="TOPIC")
    def handle(self, response, target, message, postUpdate):
        if postUpdate(message):
            return response.say(target, "Tweeted.")
        else:
            return response.say(target, "ERROR while attempting to post tweet")

    @bindFunction(message="!t (?P<tweet>.*)")
    def tweet(self, response, target, tweet, toMe, postUpdate):
        if postUpdate(tweet):
            return response.say(target, "Tweeted.")
        else:
            return response.say(target, "ERROR while attempting to post tweet")
