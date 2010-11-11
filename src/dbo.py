'''
Created on Aug 18, 2010

@author: michalracek
'''


from google.appengine.ext import db
from google.appengine.api import memcache
import logging

TRACER = logging.getLogger("sclip.dbo")

PAGE_SIZE = 5

class Image(db.Model):

    url = db.StringProperty()
    tiny =  db.BlobProperty()
    
    
    @staticmethod
    def getImage(id):
        return Image.get_by_id(id)
    

class UserInfo(db.Model):
    
    user_id = db.StringProperty(required=True)
    user = db.UserProperty(required=True)
    nick = db.StringProperty(required=True)
    
    @staticmethod
    def getUserInfo(user):
        user_info = UserInfo.all().filter('user =', user).fetch(1)
        if not user_info:
            user_info = UserInfo(user=user,user_id=user.user_id(),nick=user.nickname())
            user_info.put()
            return user_info
        else:
            return user_info[0]
    
    @staticmethod
    def getUserInfoById(user_id):
        return UserInfo.all().filter('user_id = ', user_id).fetch(1)

class Clip(db.Model):
    type = db.StringProperty(required=True)
    page = db.StringProperty(required=True)
    text = db.StringProperty()
    comment = db.StringProperty()
    title = db.StringProperty()
    link = db.StringProperty(required=False)
    src = db.StringProperty(required=False) 
    user = db.ReferenceProperty(UserInfo,required=True)
    date = db.DateTimeProperty(auto_now_add = True)
    image = db.ReferenceProperty(Image)
    likes = db.IntegerProperty(required=False)   
    
    @staticmethod
    def getPageByUser(page=0,page_size=5,user_id=None):
        user_info = UserInfo.getUserInfoById(user_id)
        if not user_info:
            return []
        q = Clip.all()
        q.filter('user = ', user_info[0])
        q.order("-date")
        return q.fetch(page_size+1,page*page_size) 
    
    @staticmethod
    def getPage(page=0,page_size=5):
        q = Clip.all()
        q.order("-date")
        return q.fetch(page_size+1,page*page_size) 
    
    @staticmethod
    def getClip(clip_id):
        return Clip.get_by_id(clip_id)
    
