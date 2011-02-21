'''
Created on Dec 1, 2010

@author: michalracek
'''

from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import datetime
from dbo import Clip,UserInfo



class UserClipLike(db.Model):
    """
    Holds reference for user which likes particular clip.
    """

    user = db.ReferenceProperty(UserInfo,required=True)
    clip = db.ReferenceProperty(Clip,required=True,collection_name="user_clip_like")
    like_date = db.DateTimeProperty(auto_now_add = True)
    
    @staticmethod
    def get_or_create(clip,user_info):
        """
        Returns existing or creates new user clip like.
        """
        if clip and user_info:
            #Get user like from DS
            user_like = clip.user_clip_like.filter("user =", user_info).fetch(1)
            #check if some user-like exists - if not, create new one
            if not user_like:
                #Create new user like do
                user_like = UserClipLike(user=user_info,clip=clip)
            else:
                user_like = user_like[0]
            #Update time stamp of the last like
            user_like.like_date = datetime.datetime.now()
            user_like.put()
            return user_like
        else:
            logging.error("Someone try to like None clip or use user_info!")
            
    @staticmethod
    def get_user_likes_query(user_info):
        """
        Returns passed user likes query
        """
        return UserClipLike.all().filter("user =", user_info).order("-like_date")
    
    @staticmethod
    def get_user_day_likes(user_info,day_date,max_clips=100):
        """
        Returns passed user likes for given day.
        """
        q = UserClipLike.all()
        q.filter('like_date >',day_date)
        q.filter('like_date <',day_date + datetime.timedelta(hours=23,minutes=59))
        q.filter('user = ', user_info)
        q.order("-like_date")
        return q.fetch(limit=max_clips)
    
    @staticmethod
    def get_user_date_likes(user_info,date_from,date_to,max_clips=100):
        """
        Returns passed user likes for given day.
        """
        q = UserClipLike.all()
        q.filter('like_date >',date_from)
        q.filter('like_date <',date_to)
        q.filter('user = ', user_info)
        q.order("-like_date")
        return q.fetch(limit=max_clips)
    
    
    @staticmethod
    def get_clip_likes(clip,max_likes=100):
        """
        Returns passed user likes query
        """
        return UserClipLike.all().filter("clip =", clip).order("-like_date").fetch(max_likes)
    
    @staticmethod
    def get_clip_user_likes(clip,user_info):
        """
        Returns passed user likes query
        """
        return UserClipLike.all().filter("clip =", clip).filter("user =", user_info).fetch(1)
    

class ClipLike(db.Model):
    """
    Like information related to particular clip.
    """
    
    clip = db.ReferenceProperty(Clip,required=False,collection_name="clip_likes")
    likes = db.IntegerProperty(required=True)
    last_like_date = db.DateTimeProperty(auto_now_add = True)
    
    @staticmethod
    def increment(clip):
        """
        Creates clip like or increase number of likes on existing like.
        """
        if clip:
            like = clip.clip_likes.fetch(1)
            #Check if like was created
            if not like:
                #Create new record for clip like
                like = ClipLike(clip=clip,likes=0)
            else:
                like = like[0]
            #Increase likes number related to the 
            like.likes = like.likes + 1
            like.put()
            return like
        else:
            logging.error("Someone try to like None clip!")
        return None
    
    @staticmethod
    def latest(count=30): 
        """
        Returns latest likes.
        """
        return ClipLike.all().order("-last_like_date").fetch(limit=count)
