'''
Created on Sep 23, 2010

@author: michalracek
'''

from google.appengine.ext import webapp
register = webapp.template.create_template_register()

#Style is defined in screen.scss
LINK_CLASS = "link-clip"
TEXT_CLASS = "text-clip"
IMAGE_CLASS = "image-clip"


def is_page_clip(clip):
    """
    Return true in case that only page is defined on clip
    """
    if clip.src and clip.src != "null":
        return False
    if clip.link and clip.link != "null":
        return False
    if clip.text and clip.text != "null":
        return False
    return True

def is_image_clip(clip):
    """
    Return true in case of image clip.
    """
    if clip.src and clip.src != "null":
        return True
    return False

def is_link_clip(clip):
    """
    Return true in case of link clip.
    """
    if not is_image_clip(clip) and clip.link and clip.link != "null":
        return True
    return False

def is_text_clip(clip):
    """
    Return true in case of text clip.
    """
    if clip.text and clip.text != "null":
        return True
    return False

def clip_class(clip):
    """
    Returns clip class according to the clip content.
    """
    if not clip:
        return "not-defined"
    if is_image_clip(clip):
        return IMAGE_CLASS
    if is_link_clip(clip) or is_page_clip(clip):
        return LINK_CLASS
    if is_text_clip(clip):
        return TEXT_CLASS
    return "not-defined"
    
register.filter(clip_class)
register.filter(is_page_clip)
register.filter(is_image_clip)
register.filter(is_link_clip)
register.filter(is_text_clip)
