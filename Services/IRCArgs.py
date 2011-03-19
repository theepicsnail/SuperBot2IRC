from Hook import bindFunction
import re
class IRCArgs:
    
    nickRE = re.compile("^(?P<nick>.*)!.*$")

    def onEvent(self,event):
        m=self.nickRE.match(event["prefix"])
        if m!=None:
            event["nick"]=m.groupdict()["nick"]
        else:
            event["nick"]=None
