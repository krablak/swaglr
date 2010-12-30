'''
Created on Dec 20, 2010

@author: michalracek

Contains various html components.

'''

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
import clips.follow.api
from dbo import UserInfo
import logging

register = webapp.template.create_template_register()

def follow_button(user_info):
    """
    Renders follow button according to follow state of the passed user. Button is displayed only for 
    logged users.
    """
    try:
        user = users.get_current_user()
        cur_user_info = UserInfo.getUserInfo(user)
        if user and user_info and (cur_user_info.key() != user_info.key()):
            if clips.follow.api.is_followed(user_info):
                return "<a id=\"follow-btn\" user=\"%s\" follow=\"no\" href=\"#\" class=\"awesome small red follow-button\">Unfollow</a>" % (user_info.nick)
            else:
                return "<a id=\"follow-btn\" user=\"%s\" follow=\"yes\" href=\"#\" class=\"awesome small blue follow-button\">Follow</a>" % (user_info.nick)
        else:
            return ""
    except:
        logging.error("Creating follow button ends with error.")
        return ""

register.filter(follow_button)
