from Hook import *

@requires("Security")
@requires("IRCArgs")
@requires("PluginManager")
class ChanTools:
    @bindFunction(command="INVITE")
    def join(self,response,message):
        return response.join(message)

    @bindFunction(command="RPL_ENDOFMOTD")
    def autoJoin(self,response):
        yield response.join("#test")
        yield response.join("#adullam")
