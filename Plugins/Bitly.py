import re
from Hook import bindFunction, requires, prefers
from Configuration import ConfigFile


AUTOLEN = 30

url = None

url_re = re.compile('(https?://[^\s]*)')

@requires("Bitly","IRCArgs")
@prefers("Colors")
class Bitly:

    @bindFunction(message="!bb")
    @bindFunction(message="!bitly")
    @bindFunction(message="!short")
    def handle(self, target, nick, toMe, message, response, shorten, colorize):
        print toMe, message, target, shorten
        if toMe:
            return #ignore pms and notices
        global url
        if url:
            short = shorten(url)
            output=""
            if colorize:
                output = colorize("{B}Shortened:{B} <{LINK}%s{}>"%short)
            else:
                output = "Shortened: <%s>"%short
            return response.say(target, output)

    @bindFunction(message="(https?://[^s]*)")
    def auto(self, message0, toMe, target, shorten, response):
        if toMe:
            return 

        global url, AUTOLEN
        url = message0
        if len(url) > AUTOLEN:
            return response.msg(target, shorten(url))
