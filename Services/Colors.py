from Hook import bindFunction
import re
class Colors:
    def color(self,msg):
        msg = msg.encode("utf-8")
        replace={
            "{}":chr(15),
            "{LINK}":chr(31)+chr(3)+"2\02\02",
            "{B}":chr(2),
            "{U}":chr(31),
            "{C}":chr(3)+"\02\02"}
        for i in range(16):
            replace["{C%i}"%i]=chr(3)+("%i\02\02"%i)
    
        for key in replace:
            msg = msg.replace(key,replace[key])
        return msg

    
    
    def onEvent(self,event):
        event["colorize"]=self.color
