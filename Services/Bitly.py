from Hook import bindFunction, requires
import re
from Configuration import ConfigFile
import urllib
import urllib2
BitlyConfig = ConfigFile("..", "Configs", "Bitly")
#Configs / Bitly.cfg
#[bitly]
#login=
#api_key=
#api_url=
if not BitlyConfig:
    raise Exception("No Bitly Configuration")


LOGIN = BitlyConfig["bitly", "login"]
API_KEY = BitlyConfig["bitly", "api_key"]
API_URL = BitlyConfig["bitly", "api_url"]
print LOGIN, API_KEY, API_URL

AUTOLEN = 30
url = None

url_re = re.compile('(https?://[^\s]*)')


@requires("IRCArgs")
class Bitly:

    def shorten(self, url):
        print "Shorten:", url
        nurl = API_URL % (LOGIN, API_KEY, urllib.quote(url))
        print "nurl:", nurl
        data = urllib2.urlopen(nurl).read()
        print "data:", data
        return "{B}Shortened:{B} <{LINK}%s{}>" % data.strip()

    def onEvent(self, event):
        event["shorten"] = self.shorten
