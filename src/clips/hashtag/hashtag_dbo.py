'''
Created on Jan 2, 2011

@author: michalracek

Data objects for clip hashtags.

'''

from google.appengine.ext import db
from google.appengine.api import memcache
from dbo import UserInfo,Clip
import logging

class HashTags(db.Model):
    """
    Clip descendant with hashtags related to clip.
    """
    
    order_date = db.DateTimeProperty(auto_now_add = True)
    tags = db.StringListProperty()
    
    @staticmethod
    def create_by_clip(clip,tags):
        """
        Creates hash tag record for clip.
        """
        if clip:
            hash_tag = HashTags(parent=clip)
            hash_tag.tags = tags
            hash_tag.put()
        else:
            logging.error("Cannot create hash tag for None clip.")    
    
    @staticmethod
    def delete_by_clip(clip):    
        if clip:
            tags = HashTags.get_by_clip(clip)
            if tags:
                tags[0].delete()
        else:
            logging.debug("Cannot delete hashtags for None clip.")
            
    @staticmethod
    def get_by_clip(clip): 
        if clip:
            result = db.GqlQuery("SELECT * FROM HashTags WHERE ANCESTOR IS :1", clip.key()).fetch(1)
            if result:
                return result[0]
