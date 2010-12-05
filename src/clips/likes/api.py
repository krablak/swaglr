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
        else:
            logging.debug("Clip with id %s was not found and cannot be liked." % (clip_id))
            
     
def get_popular_clips(clips_count=4):
    """
    Returns some most liked clips in last time.
    """
    #Get last likes
    likes = ClipLike.latest(count=10*clips_count)
    #Sort likes by the likes number
    sorted_likes = sorted(likes, key=attrgetter('likes'),reverse=True)
    #Create list of clips
    clips = []
    for i in range(0,len(sorted_likes)):
        clips.append(sorted_likes[i].clip)
    return clips


def __get_user():
    """
    Helper function to get currently logged user.
    """
    #Get logged user
    user = users.get_current_user()
    if not user:
        #Try to get user from oauth
        user = oauth.get_current_user()
    return user