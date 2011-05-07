'''
Created on Oct 12, 2010

@author: michalracek
'''
from datetime import date
from clips.api import DAY
import thirdparty.paging
import urllib

from google.appengine.api import users
from dbo import UserInfo, Clip


def to_united_clips(clips):
    return [{'day':"" , 'clips': clips}]


def page_params(req=None):
    """
    Prepares default parameters for page:
    
    user : google user representation
    greeting : user greeting URLs (see the google user api for details)
    user_info : swaglr user info representation
    """
    params = {}
    user = users.get_current_user()
    params['greeting'] = __get_greeting(user)
    if user:
        params['user'] = user
        user_info = UserInfo.getUserInfoById(user.user_id())
        if user_info:
            params['user_info'] = user_info[0]
    if req:
        params['request'] = req    
    return params

def paging(params,clips,page,max_items,user_id=None,url_prefix=None):
    """
    Prepares paging links according to loaded clips and current page number.
    """
    page_query = thirdparty.paging.PagedQuery(clips,max_items)
    if page>0 and page_query.has_page(page):
            if user_id:
                #In case that previous page is the first page, remove the page numbering from url
                if page == 1:
                    params['prev'] = urllib.quote("/user/%s/" % (user_id))
                else:
                    params['prev'] = urllib.quote("/user/%s/page/%s" % (user_id,page-1))
            else:
                if url_prefix:
                    #In case that previous page is the first page, remove the page numbering from url
                    if page == 1:
                        params['prev'] = urllib.quote("/%s/" % (url_prefix))
                    else:
                        params['prev'] = urllib.quote("/%s/page/%s" % (url_prefix,page-1))
                else:
                    #In case that previous page is the first page, remove the page numbering from url                    
                    if page == 1:
                        params['prev'] = urllib.quote("/")
                    else:
                        params['prev'] = urllib.quote("/page/%s" % (page-1))
    if  page_query.has_page(page+2):
            if user_id:
                params['next'] = urllib.quote("/user/%s/page/%s" % (user_id,page+1))
            else:
                if url_prefix:
                    params['next'] = urllib.quote("/%s/page/%s" % (url_prefix,page+1))
                else:
                    params['next'] = urllib.quote("/page/%s" % (page+1))
    if page>0:
        return page_query.fetch_page(page+1)
    else:
        return page_query.fetch(max_items)
    
    
def __get_greeting(user):
    user = users.get_current_user()
    if user:
        return ("<a class=\"awesome small\" href=\"%s\">Sign out</a>" % (users.create_logout_url("/")))
    else:
        return ("<a class=\"awesome small\" href=\"%s\">Sign in</a> </br> (You need a Google account to sign in)" % users.create_login_url("/"))
    
