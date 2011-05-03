import urllib
import urllib2
import lxml.html
from Hook import bindFunction

GOOGLE_SEARCH_URL = "http://www.google.com/search?&"


class Google:
    def _buildResponse(url, is_json=False):
        request = urllib2.Request(url, None, HEADERS)
        response = urllib2.urlopen(request)
        if is_json:
            response = simplejson.load(response)
            if not 'responseData' in response:
                return  # no data, pointless
            return response['responseData']
        return response

    def gdefine(self, term, num=None):
        """
        Returns google definition for query.

        Keyword argument:
        term -- contains query value.
        num -- Which result to return (default 0)
        """
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
