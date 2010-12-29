'''
Created on Dec 13, 2010

@author: michalracek
'''

from google.appengine.ext import db
from google.appengine.api import memcache
from dbo import UserInfo,Clip
import logging


class Followers(db.Model):
    """
    Clip descendant with followers information.
    """
    order_date = db.DateTimeProperty(auto_now_add = True)
    users = db.ListProperty(db.Key)
    
    @staticmethod
    def delete_by_clip(clip):    
        if clip:
            followers = Followers.get_by_clip(clip)
            if followers:
                followers[0].delete()
        else:
            logging.debug("Cannot delete followers for None clip.")
            
    @staticmethod
    def get_by_clip(clip): 
        if clip:
            return db.GqlQuery("SELECT * FROM Followers WHERE ANCESTOR IS :1", clip.key()).fetch(1)
    
    
class FollowedUsers(db.Model):
    """
    Users followed by another user.
    """
    
    user = db.ReferenceProperty(reference_class=UserInfo,collection_name="follow_setting")
    
    followed_users = db.ListProperty(db.Key)
    
    @staticmethod
    def get_follow_setting(user_info):
        """
        Returns information about users followed by the user passed as method argument.
        """
        follow_settings = user_info.follow_setting.fetch(1)
        if not follow_settings:
            follow_settings = FollowedUsers()
            follow_settings.user = user_info
            follow_settings.followed_users = []
            follow_settings.put()
            return follow_settings   
        else:
            return follow_settings[0]   
        
