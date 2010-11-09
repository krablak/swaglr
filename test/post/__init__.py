import urllib
import urllib2

DEV_URL = "http://localhost:8080/api/clip/post/"

def api_post(params={},url=DEV_URL):
    """
    Calls post function with parameters provided as method argument.
    """
    try:
        data = urllib.urlencode(params)
        req = urllib2.Request(DEV_URL, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        print the_page
    except urllib2.URLError, e:
        pass