'''
Created on Aug 18, 2010

@author: michalracek
'''


from google.appengine.ext import db
from google.appengine.api import memcache
import datetime
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
        if not user_info and user:
            user_info = UserInfo(user=user,user_id=user.user_id(),nick=user.nickname())
            user_info.put()
            return user_info
        else:
            if user_info:
                return user_info[0]
            else:
                return None
    
    @staticmethod
    def getUserInfoById(user_id):
        return UserInfo.all().filter('user_id = ', user_id).fetch(1)
    
    @staticmethod
    def getUserInfoFirst():
        return UserInfo.all().fetch(1)[0]
    
    @staticmethod
    def getUserInfoByNick(nick):
        return UserInfo.all().filter('nick = ', nick).fetch(1)
    

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
    def getPageByUserAndDate(user_id=None,date=None,date_from=None,max_count=100):
        user_info = UserInfo.getUserInfoById(user_id)
        if not user_info or not date:
            return []
        q = Clip.all()
        if not date_from:
            q.filter('date >',date)
            q.filter('date <',date + datetime.timedelta(hours=23,minutes=59))
        else:
            q.filter('date >',date)
            q.filter('date <',date_from)
        q.filter('user = ', user_info[0])
        q.order("-date")
        return q.fetch(max_count) 
    
    @staticmethod
    def getPage(page=0,page_size=5):
        q = Clip.all()
        q.order("-date")
        return q.fetch(page_size+1,page*page_size) 
    
    @staticmethod
    def getPagingQuery():
        q = Clip.all()
        q.order("-date")
        return q
    
    @staticmethod
    def getPageByUserQuery(user_id=None):
        user_info = UserInfo.getUserInfoById(user_id)
        if not user_info:
            return []
        q = Clip.all()
        q.filter('user = ', user_info[0])
        q.order("-date")
        return q 
    
    @staticmethod
    def getPageByUserInfoQuery(user_info):
        q = Clip.all()
        q.filter('user = ', user_info)
        q.order("-date")
        return q
    
    @staticmethod
    def getClip(clip_id):
        if clip_id:
            return Clip.get_by_id(clip_id)
        return None
    
