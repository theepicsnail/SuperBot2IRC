from Hook import *
import time
import urllib
from Logging import LogFile
log = LogFile("Mtgox")


keys=["low","buy","avg","sell","high"]

class Mtgox:
    streamSize = [0]*5
    lastData = [0]*5
    
    @dedicated(delay=10)
    def ded(self,response):
        d = dict(eval(urllib.urlopen("https://mtgox.com/api/0/data/ticker.php").read()))["ticker"]
        d = {k:round(d[k],3) for k in keys}
        vals = map(d.get,keys)

        log.dict(d,"Ticker data")
        diffs = map(lambda (x,y):x-y,zip(vals,self.lastData))
        self.lastData = vals
        change = filter(lambda x:x,diffs)!=[]
        log.debug(diffs,self.lastData,change,self.streamSize)
        if not change:
            log.debug("No change in ticker. Waiting 10 seconds")
            return 
        for idx,val in enumerate(diffs):
            log.debug("Updating Sream",idx,val)
            if val == 0:
                continue
            if val > 0:
                if self.streamSize[idx]<0:
                    self.streamSize[idx] = 0
                self.streamSize[idx]+=1
            else:
                if self.streamSize[idx]>0:
                    self.streamSize[idx] = 0
                self.streamSize[idx]-=1
    
        
        msg = " Low:{low:<10.4} Buy:{buy:<10.4} Avg:{avg:<10.4}Sell:{sell:<10.4}High:{high:<10.4}".format(**d)
        yield response.msg("#mtgoxTicker",msg)
        print self.streamSize
        yield response.msg("#mtgoxTicker",("    {:<11}"*5).format(*self.streamSize))
        

if __name__=="__main__":
    class ro:
        def msg(self,target,s):
            print target,s
    plugin = Mtgox()
    while len(samples):
        list(plugin.ded(ro()))



