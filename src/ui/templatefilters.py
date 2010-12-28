'''
Created on Sep 23, 2010

@author: michalracek
'''

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import clips.api
import clips.validations
import dbo
register = webapp.template.create_template_register()


def is_page_clip(clip):
    """
    Return true in case that only page is defined on clip
    """
    if clip:
        return clips.api.PAGE == clip.type
    return False

def is_image_clip(clip):
    """
    Return true in case of image clip.
    """
    if clip:
        return clips.api.IMAGE == clip.type
    return False

def is_link_clip(clip):
    """
    Return true in case of link clip.
    """
    if clip:
        return clips.api.LINK == clip.type
    return False

def is_text_clip(clip):
    """
    Return true in case of text clip.
    """
    if clip:
        return clips.api.TEXT == clip.type
    return False

def is_day_clip(clip):
    """
    Return true in case of day clip.
    """
    return hasattr(clip,"day")

def is_commented_clip(clip):
    """
    Returns true in case that clip is commented.
    """
    if clip:
        return clip.comment and clip.comment!=clips.validations.NULL
    return False

def is_my(clip):
    """
    Checks if the clip belongs to the current logged user.
    """
    if clip:
        user = users.get_current_user()
        if not user:
            return False
        if user.user_id() == clip.user.user_id:
            return True
    return False

def has_title(clip):
    """
    Checks if the clip has defined source page title.
    """
    if clip:
        return clip.title and clip.title!=clips.validations.NULL
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
    
def cut_url(url):
    """
    Creates short url by leaving only the domain name.
    """
    result = cut_http(url)
    result = result.split("/")[0]
    return result

def cut_http(url):
    """
    Cuts http and https prefix from the url.
    """
    result = ""
    if url:
        if url.startswith("http://"):
            result = url[7:]
        if url.startswith("https://"):
            result = url[8:]
    return result

def swag_slice(value,length):
    """
    Creates slice from passed text and add the ... html character.
    """
    if len(value)>length:
        return "%s&hellip;" % (value[:length]) 
    else:
        return value
    
def clip_template(clip,path):
    """
    Renders template with given clip as parameter.
    """
    path = os.path.join(os.path.dirname(__file__), path).replace("%sui" % (os.sep),"")
    return template.render(path, { 'clip' :clip})

def os_environ(name='HTTP_HOST'):
    return os.environ[name]


register.filter(is_page_clip)
register.filter(is_image_clip)
register.filter(is_link_clip)
register.filter(is_text_clip)
register.filter(is_day_clip)
register.filter(is_commented_clip)
register.filter(is_my)
register.filter(user_nick)
register.filter(cut_url)
register.filter(swag_slice)
register.filter(cut_http)
register.filter(clip_template)
register.filter(has_title)
register.filter(os_environ)
