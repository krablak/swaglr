'''
Created on Jan 2, 2011

@author: michalracek

Defines methods for working with hash tags.

'''
import logging
import clips.validations
from dbo import Clip
from hashtag_dbo import HashTags

TAG_DIV_CHARS = " !,?.\"/':;*(){}"

def update_hashtag_by_clip_id(clip_id):
    #Validate clip id
    clips.validations.validate_int(clip_id, "Clip id")
    #Get clip from datastore
    clip = Clip.getClip(clip_id)
    update_hashtag(clip)


def update_hashtag(clip):
    """
    Creates or updates hash tag for given clip.
    """
    if clip:
        tags = __get_tags(to_words(clip.comment))
        hashtag = HashTags.get_by_clip(clip)
        if not hashtag:
            hashtag = HashTags.create_by_clip(clip, tags=tags)
        else:
            hashtag.tags = tags
            hashtag.put()
    else:
        logging.error("Cannot update hashtags for None clip value.")
        

def get_tag_query(tag):
    """
    Get tags query for the specified tag.
    """
    if tag:
        return HashTags.all().filter("tags =",tag).order("-order_date")
    else:
        return None

def get_clips_by_tags(tags_keys):
    if tags_keys:
        clip_keys = []
        for key in tags_keys:
            if key.parent():
                clip_keys.append(key.parent().key())
        return Clip.get(clip_keys)

def __get_tags(comment_words=""):
    """
    Get tags within the passed comment
    """
    tags = []
    if comment_words:
        for word in comment_words:
            if is_tag(word["word"]):
                tags.append(word["word"])
    return tags


def is_tag(word):
    """
    Returns True in case that word is hash tag.
    """
    return word and word.startswith("#") and len(word)>0


def to_words(comment):
    """
    Converts comment text to array of words and delimiters.
    """
    result = []
    word = ""
    if comment:        
        for char in comment:
            if char in TAG_DIV_CHARS:
                result.append({"word" : word,"post" : char})
                word = ""
            else:
                word = word + char
    if word:
        result.append({"word" : word,"post" : ''})
    return result