'''
Created on Sep 23, 2010

@author: michalracek
'''

from google.appengine.ext import webapp
from google.appengine.api import users
import clips.api
import clips.validations
import dbo
register = webapp.template.create_template_register()


def is_page_clip(clip):
    """
    Return true in case that only page is defined on clip
    """
    return clips.api.PAGE == clip.type

def is_image_clip(clip):
    """
    Return true in case of image clip.
    """
    return clips.api.IMAGE == clip.type

def is_link_clip(clip):
    """
    Return true in case of link clip.
    """
    return clips.api.LINK == clip.type

def is_text_clip(clip):
    """
    Return true in case of text clip.
    """
    return clips.api.TEXT == clip.type

def is_commented_clip(clip):
    """
    Returns true in case that clip is commented.
    """
    return clip.comment and clip.comment!=clips.validations.NULL

def is_my(clip):
    """
    Checks if the clip belongs to the current logged user.
    """
    user = users.get_current_user()
    if not user:
        return False
    if user.user_id() == clip.user.user_id:
        return True
    return False

def user_nick(user):
    """
    Get user nic defined by user settings.
    """
    user = users.get_current_user()
    if not user:
        return False
    else:
        return dbo.UserInfo.getUserInfo(user).nick


register.filter(is_page_clip)
register.filter(is_image_clip)
register.filter(is_link_clip)
register.filter(is_text_clip)
register.filter(is_commented_clip)
register.filter(is_my)
register.filter(user_nick)