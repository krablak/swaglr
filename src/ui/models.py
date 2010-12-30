'''
Created on Oct 12, 2010

@author: michalracek
'''
from datetime import date
from clips.api import DAY
import thirdparty.paging

from google.appengine.api import users
from dbo import UserInfo, Clip

UNKNOWN_DATE_TEXT = "in the year one";
TODAY = "today"
YESTERDAY = "yesterday"
OLDER = "%s days ago"

def to_day_clips(clips):
    """
    Creates page model from list of clips.
    """
    #Clips model divided to day based dict
    days_model = {}
    #Holds order of the days- instead of dict keys
    days_order = []
    if clips:
        #Go over each clip and add it into days model according to humanized date.
        for clip in clips:
            #Create humanized date string
            str_date = __to_humanized_date(clip.date)
            #Check if model has record for this date.
            if not days_model.has_key(str_date):
                days_model[str_date] = []
                #Add day into ordered list
                days_order.insert(0,str_date)
            #Append clip into model by date
            days_model[str_date].append(clip)
    #Covert to list- due to Django templates 0.96 which is not able to iterate over dict :(
    for day in days_order:
        if days_model[day]:
            if not day==TODAY:
                days_model[day][0].day = day
    result_list = []
    for day in days_order:
        result_list = days_model[day] + result_list
    return [{'day':"" , 'clips': result_list}]

def to_united_clips(clips):
    return [{'day':"" , 'clips': clips}]

def __to_humanized_date(robotic_date):
    """
    Converts date time into human readable string.
    """
    if date:
        try:
            delta = date(robotic_date.year, robotic_date.month, robotic_date.day) - date.today()
            days = delta.days
            if days == 0:
                return TODAY
            if days == -1:
                return YESTERDAY
            else:
                return OLDER % (days*-1)
        except AttributeError:
            pass
        except ValueError:
            pass
    return UNKNOWN_DATE_TEXT

def page_params():
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
    return params

def paging(params,clips,page,max_items,user_id=None,url_prefix=None):
    """
    Prepares paging links according to loaded clips and current page number.
    """
    page_query = thirdparty.paging.PagedQuery(clips,max_items)
    if page>0 and page_query.has_page(page):
            if user_id:
                params['prev'] = "/user/%s/page/%s" % (user_id,page-1)
            else:
                if url_prefix:
                    params['prev'] = "/%s/%s" % (url_prefix,page-1)
                else:
                    params['prev'] = "/page/%s" % (page-1)
    if  page_query.has_page(page+1):
            if user_id:
                params['next'] = "/user/%s/page/%s" % (user_id,page+1)
            else:
                if url_prefix:
                    params['next'] = "/%s/%s" % (url_prefix,page+1)
                else:
                    params['next'] = "/page/%s" % (page+1)
    if page>0:
        return page_query.fetch_page(page+1)
    else:
        return page_query.fetch(max_items)
    
    
def __get_greeting(user):
    user = users.get_current_user()
    if user:
        return ("<a class=\"awesome small\" href=\"%s\">Sign out</a>" % (users.create_logout_url("/")))
    else:
        return ("<a class=\"awesome small\" href=\"%s\">Sign in</a>" % users.create_login_url("/"))
    
