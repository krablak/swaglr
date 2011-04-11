'''
Created on Dec 7, 2010

@author: michalracek

Contains functionality for embeded content.

'''
from google.appengine.ext import webapp
import embed.youtube
import embed.vimeo
register = webapp.template.create_template_register()


def is_embed_content(clip):
    """
    Checks if clip is one of the supported embeded contents.
    """
    try:
        return embed.youtube.is_embed_content(clip) or embed.vimeo.is_embed_content(clip)
    except:
        return False

def get_embed_content(clip):
    """
    Returns clip embed HTML content.
    """
    try:
        #Check if url match to youtube video
        if embed.youtube.is_embed_content(clip):
            return embed.youtube.get_embed_content(clip)
        if embed.vimeo.is_embed_content(clip):
            return embed.vimeo.get_embed_content(clip)
    except:
        pass
    return clip.page

def get_embed_preview_url(clip):
    """
    Returns clip embed preview url or None in case that preview image does not exist.
    """
    try:
        #Check if url match to youtube video
        if embed.youtube.is_embed_content(clip):
            return embed.youtube.get_preview_url(clip)
        if embed.vimeo.is_embed_content(clip):
            return None
    except:
        pass
    return None
    

register.filter(is_embed_content)
register.filter(get_embed_content)
register.filter(get_embed_preview_url)
