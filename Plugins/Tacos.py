from Hook import *
from Logging import LogFile
log = LogFile("Tacos")


@requires("IRCArgs")
@requires("Colors")
class Tacos:
    @bindFunction(message="!tacos")   
    def beef(self, nick, target, response, colorize):
        if colorize:
            cheesy = colorize("{U}Me gusta!!{U}")
        else:
            cheesy = "Me gusta!!"
        return response.say(target, cheesy)

