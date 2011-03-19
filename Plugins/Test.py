from Hook import bindFunction,requires

@requires("Security")
class Test:
    @bindFunction(command="PRIVMSG",prefix="(?P<nick>.*)!.*")
    def foo(self,response,nick,message,loggedIn):
        if loggedIn(nick):
            return response.msg(nick,message);
            
        if message=="stop":
            return response.stop()
        
    @bindFunction(message="!count (?P<start>\\d+) (?P<end>\\d+)",prefix="(?P<nick>.*)!.*")
    def count(self,response,start,end,nick):
        for i in xrange(int(start),int(end), 1 if start < end else -1):
            yield response.msg(nick,str(i))

    @bindFunction(message="A")
    @bindFunction(message="B")
    def ab(self,response):
        return response.msg("snail","abc")
