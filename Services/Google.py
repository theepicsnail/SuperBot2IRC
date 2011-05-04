import urllib
import urllib2
import lxml.html
from Hook import bindFunction

GOOGLE_SEARCH_URL = "http://www.google.com/search?&"
HEADERS  = { 'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5)" }


class Google:
    def _buildResponse(self, url, is_json=False):
        request = urllib2.Request(url, None, HEADERS)
        response = urllib2.urlopen(request)
        if is_json:
            response = simplejson.load(response)
            if not 'responseData' in response:
                return  # no data, pointless
            return response['responseData']
        return response

    def gdefine(self, term, num=0):
        """
        Returns google definition for query.

        Keyword argument:
        term -- contains query value.
        num -- Which result to return (default 0)
        """
        if num == '':
            num = 0
        num = int(num)

        query = { 'q': 'define:' + term }
        url = GOOGLE_SEARCH_URL + urllib.urlencode(query)
        response = self._buildResponse(url)
        html = response.read()
        pdoc = lxml.html.fromstring(html)
        results = pdoc.body.cssselect('ul.std li')
        result = results[num].text.strip()
        link = "No link."
        try:
            link = 'http://' + pdoc.body.cssselect('ul.std li a')[num].text_content()
        except IndexError:
            pass
        return (result, link, num, len(results) - 1)

    def onEvent(self, event):
        event["gdefine"] = self.gdefine
