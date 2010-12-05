'''
Created on Oct 12, 2010

@author: michalracek
'''
from datetime import date

def to_day_clips(clips):
    """
    Creates page model from list of clips.
    """
    #Clips model divided to day based dict
    days_model = {}
    #Holds order of the days- instead of dict keys
    days_order = []
    #Go over each clip and add it into days model according to humanized date.
    for clip in clips:
        #Create humanized date string
        str_date = __to_humanized_date(clip.date)
        print "Humanized date: %s" % (str_date)
        #Check if model has record for this date.
        if not days_model.has_key(str_date):
            days_model[str_date] = []
            #Add day into ordered list
            days_order.insert(0,str_date)
        #Append clip into model by date
        days_model[str_date].append(clip)
    #Covert to list- due to Django templates 0.96 which is not able to iterate over dict :(
    days_model_list = []
    for day in days_order:
        days_model_list.insert(0,{'day':day , 'clips': days_model[day]})    
    return days_model_list

def __to_page_clip(clip):
    return None


UNKNOWN_DATE_TEXT = "in the year one";
def __to_humanized_date(robotic_date):
    """
    Converts date time into human readable string.
    """
    if date:
        try:
            delta = date(robotic_date.year, robotic_date.month, robotic_date.day) - date.today()
            days = delta.days
            if days == 0:
                return "today"
            if days == -1:
                return "yesterday"
            else:
                return "%s days ago" % (days*-1)
        except AttributeError:
            pass
        except ValueError:
            pass
    return UNKNOWN_DATE_TEXT

from google.appengine.api import users
from dbo import UserInfo

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

def paging(params,clips,page,max_items,user_id=None):
    """
    Prepares paging links according to loaded clips and current page number.
    """
    if len(clips)>max_items:
            if user_id:
                params['prev'] = "/user/%s/page/%s" % (user_id,page+1)
            else:
                params['prev'] = "/page/%s" % (page+1)
            clips = clips[0:-1]
    if page>0:
            if user_id:
                params['next'] = "/user/%s/page/%s" % (user_id,page-1)
            else:
                params['next'] = "/page/%s" % (page-1)
            if len(clips)>0:
                clips = clips[0:-1]
    
    
def __get_greeting(user):
    user = users.get_current_user()
    if user:
        return ("<a href=\"%s\">Sign out</a>" % (users.create_logout_url("/")))
    else:
        return ("<a href=\"%s\">Sign in</a>" % users.create_login_url("/"))
    
