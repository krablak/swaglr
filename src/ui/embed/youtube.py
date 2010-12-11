'''
Created on Dec 7, 2010

@author: michalracek

Support methods for youtube videos
'''
from google.appengine.ext import webapp
import ui.templatefilters

def is_embed_content(clip):
    """
    Checks if clip is one of the supported embeded contents.
    """
    if ui.templatefilters.is_link_clip(clip) or ui.templatefilters.is_page_clip(clip):
        #Check if url match to youtube video
        if "http://www.youtube.com/watch?v=" in clip.page:
            return True
    return False

def get_embed_content(clip):
    """
    Returns clip embed HTML content.
    """
    #Check if url match to youtube video
    if "http://www.youtube.com/watch?v=" in clip.page:
        if clip.page.find("?")!=-1:
            video_id = ""
            if clip.page.find("&")!=-1:
                video_id = clip.page[len("http://www.youtube.com/watch?v="):clip.page.find("&")]
            else:
                video_id = clip.page[len("http://www.youtube.com/watch?v="):]
            return "<object width=\"390\" height=\"290\"><param name=\"movie\" value=\"http://www.youtube.com/v/%s?fs=1&amp;hl=en_US\"></param><param name=\"allowFullScreen\" value=\"true\"></param><param name=\"allowscriptaccess\" value=\"always\"></param><embed src=\"http://www.youtube.com/v/%s?fs=1&amp;hl=en_US\" type=\"application/x-shockwave-flash\" allowscriptaccess=\"always\" allowfullscreen=\"true\" width=\"390\" height=\"290\"></embed></object>" % (video_id,video_id)
    return clip.page
