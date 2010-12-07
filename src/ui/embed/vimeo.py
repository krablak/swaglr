'''
Created on Dec 7, 2010

@author: michalracek

Support methods for youtube videos
'''

import ui.templatefilters

def is_embed_content(clip):
    """
    Checks if clip is one of the supported embeded contents.
    """
    if ui.templatefilters.is_link_clip(clip) or ui.templatefilters.is_page_clip(clip):
        #Check if url match to youtube video
        if "http://vimeo.com/" in clip.page:
            try:
                clip_id = int(clip.page[len("http://vimeo.com/"):])
                return clip_id
            except:
                pass
    return False

def get_embed_content(clip):
    """
    Returns clip embed HTML content.
    """
    """
    """
    #Check if url match to vimeo video
    video_id = is_embed_content(clip)
    if video_id:
        return "<iframe src=\"http://player.vimeo.com/video/%s\" width=\"390\" height=\"290\" frameborder=\"0\"></iframe>" % (video_id)
    return clip.page
