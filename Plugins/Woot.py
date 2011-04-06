from Hook import bindFunction
import urllib2
import re

name = re.compile("<h2 class=\"fn\">(.*)</h2>")
price= re.compile("amount\">(.*?)<")
class Woot:
    @bindFunction(message="!woot")
    def woot(self,message,target,response):
        data = urllib2.urlopen("http://www.woot.com").read() 
        n = name.search(data)
        p = price.search(data)
        if n and p:
            n = n.groups()[0]
            p = p.groups()[0]
            return response.say(target,"Woot:%s %s"%(p,n))
        else:
            return response.say(target,"Failed to woot :(")
