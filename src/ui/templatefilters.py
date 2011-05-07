'''
Created on Sep 23, 2010

@author: michalracek
'''

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import clips.api
import clips.likes.api
import clips.validations
import clips.hashtag.api
import ui.embedfilters
import dbo
import cgi
import urllib


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
    return __short_value(value,length,"...")

def to_tag_comment(comment):
    """
    Replace hashtags with liks to tag reports.
    """
    if comment:
        if comment == "null":
            comment = ""
        result = []
        comment = cgi.escape(comment)
        words = clips.hashtag.api.to_words(comment)
        for word in words:
            if clips.hashtag.api.is_tag(word["word"]):
                escaped_word = cgi.escape(word["word"])
                result.append("<a href=\"/swags/tagged/as/%s/\">%s</a>%s" % (urllib.quote(escaped_word).lower(),escaped_word,word["post"]))
            else:
                result.append(word["word"]+word["post"])
        return "".join(result)
    return comment

def is_liked(clip):
    """
    Returns True in case that clip is liked by current user.
    """
    return clips.likes.api.is_liked(None, clip)
    
def clip_template(clip,path):
    """
    Renders template with given clip as parameter.
    """
    path = os.path.join(os.path.dirname(__file__), path).replace("%sui" % (os.sep),"")
    return template.render(path, { 'clip' :clip})

def os_environ(name='HTTP_HOST'):
    return os.environ[name]

def is_user_home(request):
    """
    Return true in case that user is logged in and is on his home page.
    """
    user = users.get_current_user()
    if not user:
        return False
    else:
        return request.path == "/"
    
def is_main_page(request):
    """
    Returns true in case of ain page url
    """
    return request.path == "/"

def share_text(clip):
    """
    Returns text used for sharing created by following rules:
        1) If the clip is commented the shorted comment is returned.
        2) If clip is text the  shorted text is returned.
        3) If clip is page the shorted title is returned.
        4) If clip is link the cut url is returned.
        5) If clip is image the cut url is returned.
    """
    if clip:
        if is_commented_clip(clip):
            value = clip.comment
            return __short_value(value,100,"...")
        if is_text_clip(clip):
            value = clip.text
            value = __short_value(value,100,"...")
            return "\"%s\"" % (value)
        if is_page_clip(clip):
            value = ""
            if ui.embedfilters.is_embed_content(clip):
                text = ui.embedfilters.get_embed_preview_share_text(clip)
                value = clip.title
                value = __short_value(value,100,"...")
                return "%s %s" % (text,value)
            else:
                value = clip.title
                value = __short_value(value,100,"...")
                return "check the page %s" % (value)
        if is_link_clip(clip):
            value = clip.link
            value = cut_url(value)
            value = __short_value(value,50,"...")
            return "nice link to %s" % (value)
        if is_image_clip(clip):
            value = clip.page
            value = cut_url(value)
            return "nice pic at %s" % (value)
    return "Something quoted on SWAGLR"

def __short_value(value,length,endchar):
    """
    Helper function to short values.
    """
    if len(value)>length:
        return "%s%s" % (value[:length],endchar) 
    else:
        return value


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
register.filter(to_tag_comment)
register.filter(is_liked)
register.filter(is_user_home)
register.filter(is_main_page)
register.filter(share_text)

