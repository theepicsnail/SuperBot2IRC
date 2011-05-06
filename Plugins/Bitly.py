import re
from Hook import bindFunction, requires, prefers
from Configuration import ConfigFile

AUTOLEN = 30

url = None


@requires("Bitly", "IRCArgs")
@prefers("Colors")
class Bitly:
    @bindFunction(message="!bb")
    @bindFunction(message="!bitly")
    @bindFunction(message="!short")
    def handle(self, target, nick, toMe, message, response, colorize, shorten):
        if toMe:
            return  # ignore pms and notices
        global url
        print('Shortening %s' % url)
        if url:
            short = shorten(url)
            print(short)
            output = ""
            if colorize:
                output = colorize("{B}Shortened:{B} <{LINK}%s{}>" % short)
            else:
                output = "Shortened: <%s>" % short
            return response.say(target, output)

    @bindFunction(message="(https?://[^\s!,]*)")
    def auto(self, message0, toMe, target, response, colorize, shorten):
        print(toMe, target, len(message0), message0)
        if toMe:
            return

        global url, AUTOLEN
        url = message0
        if len(url) > AUTOLEN:
            short = shorten(url)
            print(short)
            output = ""
            if colorize:
                output = colorize("{B}Shortened:{B} <{LINK}%s{}>" % short)
            else:
                output = "Shortened: <%s>" % short
            return response.say(target, output)
