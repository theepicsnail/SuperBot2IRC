from Hook import *

@requires("IRCArgs")
class ChanTools:
    @bindFunction(command="INVITE")
    def join(self,response,message):
        return response.join(message)

    @bindFunction(command="RPL_ENDOFMOTD")
    def autoJoin(self,response):
        yield response.join("#test")
        yield response.join("#adullam")

    @bindFunction(message="^(?P<stuff>.*)\\o/")
    def yayMan(self,response, stuff, target):
        spaces = (len(stuff)-1)*" "
        yield response.msg(target,spaces+"YAY")
        yield response.msg(target,spaces+"/ \\")
