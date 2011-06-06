import urllib
import urllib2
import lxml.html
from Hook import bindFunction
from Logging import LogFile
log = LogFile("GoogleService")
GOOGLE_SEARCH_URL = "http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&sl=en&tl=en&restrict=pr%2Cde&client=te&"
HEADERS  = { 'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5)" }


class Google:
    def _buildResponse(self, url, is_json=False):
        log.debug("Build request",url,is_json)
        request = urllib2.Request(url, None, HEADERS)
        response = urllib2.urlopen(request)
        if is_json:
            response = simplejson.load(response)
            if not 'responseData' in response:
                log.warning("Json response was empty")
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

        log.debug("gdefine",term,num)

        if num == '':
            num = 0
        num = int(num)

        query = { 'q': term }
        url = GOOGLE_SEARCH_URL+ urllib.urlencode(query)
        response = self._buildResponse(url) 
        data = response.read()
        try:
            null=None
            db = eval(data[24:])
        except:
            log.exception()
            pass
        results =db[0]["webDefinitions"][0]["entries"]
        result = results[num]["terms"][0]["text"]
        return (result, num, len(results) - 1)

    def onEvent(self, event):
        event["gdefine"] = self.gdefine
