'''
Created on Nov 29, 2010

@author: michalracek

Defines interface for swag likes.
'''

import logging
from google.appengine.api import users,oauth

from dbo import Clip,UserInfo
from like_dbo import ClipLike,UserClipLike
import clips.validations
from operator import itemgetter, attrgetter


def like(id):
    """
    Adds like to existing clip.
    """
    clip_id = clips.validations.to_int_param(id)
    #Check if clip id was correcly converted to int.
    if clip_id == 0:
        logging.error("Cannot like clip with id %s" % (clip_id))
    else:
        logging.debug("Starting like for clip with id %s" % (clip_id))            
        #Try to get clip from DS
        clip = Clip.getClip(clip_id)
        #Check if clip was found
        if clip:
            #Check if like was done by logged user
            user = __get_user()
            if user:
                #User is logged in and the user like will be created
                user_info = UserInfo.getUserInfo(user)
                UserClipLike.get_or_create(clip, user_info)
            #Increase clip like
            ClipLike.increment(clip)
            #Increase clip count
            if not clip.likes:
                clip.likes = 0;
            clip.likes = clip.likes + 1
            clip.put()    
        else:
            logging.debug("Clip with id %s was not found and cannot be liked." % (clip_id))
            
def is_liked(user_info,clip):
    """
    Checks if passed clip is liked by the passed user.
    """
    if not user_info:
        user_info = UserInfo.getUserInfo(__get_user())
    if clip and user_info:
        return UserClipLike.get_clip_user_likes(clip, user_info)
    return True
            
     
def get_popular_clips(clips_count=4):
    """
    Returns some most liked clips in last time.
    """
    #Get last likes
    likes = ClipLike.latest(count=clips_count)
    #Sort likes by the likes number
    sorted_likes = sorted(likes, key=attrgetter('likes'),reverse=True)
    #Create list of clips
    clips = []
    for i in range(0,len(sorted_likes)):
        try:
            clips.append(sorted_likes[i].clip)
        except:
            logging.error("Cannot read clip reference from user like %s" %(sorted_likes[i]))
    return clips

def get_liked_by_query(user_info):
    """
    Returns likes liked by passed user.
    """
    if user_info:
        return UserClipLike.get_user_likes_query(user_info)
    return None

def get_clips_by_user_likes(user_likes):
    """
    Returns clips liked by passed user.
    """
    if user_likes:
        clip_keys = [ user_like.clip.key() for user_like in user_likes]
        return Clip.get(clip_keys)
    return None

def get_day_clips_by_user_likes(user_info,day_date=None,date_to=None):
    """
    Returns clips liked by passed user in specified date.
    """
    if user_info and day_date:
        #Get user likes for given date
        user_likes = []
        if not date_to:
            user_likes = UserClipLike.get_user_day_likes(user_info, day_date)
        else:        
            user_likes = UserClipLike.get_user_date_likes(user_info, day_date,date_to)
        #Get clip keys and load clips by the found user likes
        clip_keys = [ user_like.clip.key() for user_like in user_likes]
        return Clip.get(clip_keys)
    else:
        logging.error("Cannot get user likes for user '%s' and date '%s'" % (user_info,day_date))
    return None

def get_user_likes_by_clip(clip):
    """
    Returns user likes for given clip.
    """
    if clip:
        return UserClipLike.get_clip_likes(clip)
    else:
        return []

def __get_user():
    """
    Helper function to get currently logged user.
    """
    #Get logged user
    user = users.get_current_user()
    return user