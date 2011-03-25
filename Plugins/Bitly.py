from Hook import bindFunction,requires
import re
from Configuration import ConfigFile


AUTOLEN=30

url =None

url_re = re.compile('(https?://[^\s]*)')

@requires("IRCArgs","Bitly")
class Bitly:
    
    @bindFunction(message="!bb")
    @bindFunction(message="!bitly")
    @bindFunction(message="!short")
    def handle(self,target,nick,toMe, message,response,shorten):
        print toMe,message,target,shorten
        if toMe: return #ignore pms and notices
        global url
        if url:
            return response.say(target, shorten(url))

    @bindFunction(message="(https?://[^s]*)")
    def auto(self,message0,toMe,target,shorten):
        if toMe: return 

        global url,AUTOLEN
        url = message0
        if len(url)>AUTOLEN:
            return response.msg(target,shorten(url))
        


        
