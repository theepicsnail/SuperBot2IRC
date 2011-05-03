from Hook import *

@requires("Security")
@requires("IRCArgs")
@requires("PluginManager")
class ChanTools:
    @bindFunction(command="PRIVMSG")
    def foo(self,response,nick,message,loggedIn):
        if loggedIn(nick):
            return response.msg(nick,message);
            
        if message=="stop":
            return response.stop()
        
    @bindFunction(message="!count (?P<start>\\d+) (?P<end>\\d+)")
    def count(self,response,start,end,nick,target,toMe):
        if toMe: target = nick

        for i in xrange(int(start),int(end), 1 if start < end else -1):
            yield response.msg(target,str(i))

    @bindFunction(command="INVITE")
    def join(self,response,message):
        return response.join(message)

    @bindFunction(command="RPL_ENDOFMOTD")
    def autoJoin(self,response):
        return response.join("#test")
