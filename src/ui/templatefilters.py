'''
Created on Sep 23, 2010

@author: michalracek
'''

from google.appengine.ext import webapp
import clips.api
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


register.filter(is_page_clip)
register.filter(is_image_clip)
register.filter(is_link_clip)
register.filter(is_text_clip)
