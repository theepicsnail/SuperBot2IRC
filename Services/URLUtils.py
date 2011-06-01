import re
import urllib2
# Try lxml, fall back to BeautifulSoup, keep falling to string parsing
try:
    import lxml.html
except ImportError:
    lxml = False

try:
    from BeautifulSoup import BeautifulSoup, BeautifulStoneSoups
except ImportError:
    import htmlentitydefs
    import re
    BeautifulStone = False


class URLUtils:
    def grabTitle(self, url):
        """Return the title of the page if exists."""
        try:
            pagepart = urllib2.urlopen(url, None, 5).read(5120)
            if lxml:
                title = lxml.html.fromstring(pagepart).find(".//title").text
                return re.sub('[\n\r\t ]+', ' ', title).strip()
            elif BeautifulSoup:
                title = BeautifulSoup(pagepart)
                title = re.sub('[\n\r\t ]+', ' ', title).strip()
                return BeautifulStoneSoup(title, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
            else:
                title = pagepart.split("title>")[1][:-2]
                title = re.sub('[\n\r\t ]+', ' ', title).strip()
                return self.unescape(str(title))
        except Exception, e:
            raise e

    # taken from http://effbot.org/zone/re-sub.htm#unescape-html
    # Written by Fredrik Lundh
    def unescape(self, text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text  # leave as is
        return re.sub("&#?\w+;", fixup, text)

    def onEvent(self, event):
        event["grabTitle"] = self.grabTitle
