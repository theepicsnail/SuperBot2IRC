from Hook import *
import time
import urllib
class Mtgox:
    last = ""
    @dedicated()
    def ded(self,response):
        
        d = dict(eval(urllib.urlopen("https://mtgox.com/api/0/data/ticker.php").read()))
        msg = "Low:{low:<10.3}Buy:{buy:<10.3}Avg:{avg:<10.3}Sell:{sell:<10.3}High:{high:<10.3}".format(**d["ticker"])

        if msg != self.last:
            yield response.msg("#mtgoxTicker",msg)
            time.sleep(85)
        self.last = msg
