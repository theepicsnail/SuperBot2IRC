from Hook import bindFunction,prefers
from Logging import LogFile
import re


log = LogFile("Sed")
msgHistory = [""]*10

@prefers("Colors")
class Sed:

    @bindFunction(message="!s(.)(?P<search>.*)\\1(?P<replace>.*)\\1(?P<flags>.*)")
    def doIt(self,search,replace,flags,response,colorize,target):
        global msgHistory
        log.debug("Sed matching", search,replace,flags,response,colorize)
        if flags.find("i")+1:
            search = re.compile(search,re.I)
        else:
            search = re.compile(search)
        log.debug("search:",search) 
        for i in msgHistory:
            res = search.search(i)
            log.debug("Search Result:",i,res)
            if res:
                colored = flags.find("c")+1 and colorize
                if colored:
                    replace = "{C3}%s{}"%replace
                elif flags.find("c")+1:
                    yield response.say(target,"'Colors' service wasn't loaded.")

                
                log.debug("Replace,flags",replace,flags,flags.find("g")+1 and colorize)
            
                if flags.find("g")+1:
                    out = search.sub(replace,i,0)
                else:
                    out = search.sub(replace,i,1)

                if colored:
                    out = colorize(out)

                yield response.say(target,out)
                return                 

    @bindFunction(command="PRIVMSG",message="^[^!]")
    def record(self,message):
        global msgHistory
        log.debug("Sed recording.",msgHistory)
        msgHistory=[message]+msgHistory[:-1]
        
