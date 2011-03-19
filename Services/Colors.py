from Hook import bindFunction
import re
class Colors:
    
    def onEvent(self,event):
        m=self.nickRE.match(event["prefix"])
        if m!=None:
            event["nick"]=m.groupdict()["nick"]
        else:
            event["nick"]=None
