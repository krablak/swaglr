'''
Created on Nov 9, 2010

@author: michalracek
'''
import urllib
import urllib2
import simplejson

DEV_URL = "http://localhost:8080/api/clip/post/"

def post(params={},server_url=DEV_URL,verbose=False):
    """
    Post the clip using the swaglr RPC method.
    
    params (required): dictionary with the following keys:
        type (required) : Type of posted clip. Allowed values:
                TEXT : used for text citations post.
                LINK : used for link post.
                IMAGE : used for image post.
                PAGE : used for page post.
                
        text (required for type TEXT) : post text.
        link (required for type LINK) : post link URL.
        src (required for type IMAGE) : post image URL. Image must be at public available url. 
        page (required for type PAGE) : post web page URL.
        title (optional for type PAGE) : post web page Title.   
    
    server_url : URL of swaglr server.
    
    Returns dict with the following keys:
        code : OK in case of successful post otherwise returns 'ERROR'. 
        desc : Human readable description of performed operation.
    """
    try:
        data = urllib.urlencode(params)
        req = urllib2.Request(DEV_URL, data)
        response = urllib2.urlopen(req)
        data = response.read()
        parsed_date = simplejson.loads(data)
        res_code = parsed_date['code']
        res_desc = parsed_date['desc']
        if verbose:
            print "Code: '%s'  Desc: '%s'" % (res_code,res_desc)
        return {'code' : res_code , 'desc' : res_desc}
    except urllib2.URLError, e:
        return {'ERROR' : "Cannot reach the swaglr at url '%s'" % (server_url)}
    

