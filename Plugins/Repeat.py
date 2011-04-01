from Hook import *


@requires("IRCArgs")  # provides 'nick' args
class Repeat:

    @bindFunction(message="!repeat (.*)")
    def repeat(self, response, nick, message0):
        return response.msg(nick, message0)
