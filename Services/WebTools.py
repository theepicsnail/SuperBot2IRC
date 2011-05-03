"""Useful tools for opening and reading pages."""
 
from urllib2 import Request, build_opener, urlopen, URLError, HTTPError
 
import sys
 
from Logging import LogFile
 
log = LogFile("URLUtils")
 
class URLUtils(object):
   
    USER_AGENT = ('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT')
 
    def open_url(self, url):
        """Simply open and return page contents mimicking a browser."""
        
        request = Request(url, None)
        opener = build_opener()
        opener.add_headers = [self.USER_AGENT]
 
        try:
            response = opener.open(request)
        except HTTPError, e:
            log.exception("There server couldn't fulfill the request.", "Error: %s" % e.code, "URL: %s" % url)
        except URLError, e:
            log.exception("Failed to reach a server.", "Error: %s" % e.code, "URL: %s" % url)
        else:
            return response.read()
 
    def open_url_lxml(self, url):
        """Returns an lxml object on the corresponding url."""
        try:
            import lxml.html
        except ImportError:
            log.exception("open_url_lxml called but lxml not installed")
 
        return lxml.html.fromstring(self.open_url(url))
 
    def open_url_bsoup(self, url):
        """Returns an BeautifulSoup object on the corresponding url."""
        try:
            from BeautifulSoup import BeautifulSoup as bs
        except ImportError:
            log.exception("open_url_bsoup called but BeautifulSoup not installed")
 
        return bs(self.open_url(url))
 
    def onEvent(self, event):
        event['open_url'] = self.open_url
        event['open_url_lxml'] = self.open_url_lxml
        event['open_url_bsoup'] = self.open_url_bsoup

