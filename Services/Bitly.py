from Hook import bindFunction,requires
import re
from Configuration import ConfigFile
import urllib,urllib2
BitlyConfig=ConfigFile("..","Configs","Bitly")
#Configs/Bitly.cfg
#[bitly]
#login=
#api_key=
#api_url=
if not BitlyConfig:
    raise Exception("No Bitly Configuration")


LOGIN = BitlyConfig["bitly","login"]
API_KEY = BitlyConfig["bitly","api_key"]
API_URL = BitlyConfig["bitly","api_url"]
print LOGIN,API_KEY,API_URL

AUTOLEN=30
url =None

url_re = re.compile('(https?://[^\s]*)')

@requires("IRCArgs")
class Bitly:

    def shorten(self,url):
        nurl = API_URL%(LOGIN, API_KEY, urllib.quote(url))
        data = urllib2.urlopen(nurl).read()
        return data.strip()


    def onEvent(self,event):
        event["shorten"]=self.shorten
    
        


        
