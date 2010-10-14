'''
Created on Aug 18, 2010

@author: michalracek
'''

import logging
import util
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import oauth
from image import thumbnail
import ui.models
from ui.error_logging import log_errors
from dbo import *
import datetime
import dbo

PAGING = 20

class MainPage(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        #Get all events
        clips = Clip.getPage(0,PAGING)
        if len(clips)>PAGING:
            params['prev'] = "/page/%s" % (1)
            clips = clips[0:-1]
        params['day_clips'] = ui.models.to_day_clips(clips)
        util.render("templates/index.html", params, self.response)
        
class Paging(webapp.RequestHandler):    
    
    @log_errors
    def get(self,page_val):
        page = 0    
        try:
            page = int(page_val)
        except:
            pass
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        #Get all events
        clips = Clip.getPage(page, PAGING)
        if len(clips)>PAGING:
            params['prev'] = "/page/%s" % (page+1)
            clips = clips[0:-1]
        if page>0:
            params['next'] = "/page/%s" % (page-1)            
        params['day_clips'] = ui.models.to_day_clips(clips)
        util.render("templates/index.html", params, self.response)
        
class User(webapp.RequestHandler):    
    
    @log_errors
    def get(self,user_id_val,page_val):
        user_id = ""
        try:
            user_id = str(user_id_val)
        except:
            pass
        page = 0    
        try:
            page = int(page_val)
        except:
            pass
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        #Get all events
        clips = Clip.getPageByUser(page, PAGING, user_id)
        if len(clips)>PAGING:
            params['prev'] = "/user/%s/page/%s" % (user_id,page+1)
            clips = clips[0:-1]
        if page>0:
            params['next'] = "/user/%s/page/%s" % (user_id,page-1)            
        params['day_clips'] = ui.models.to_day_clips(clips)
        util.render("templates/index.html", params, self.response)
        

        
class Detail(webapp.RequestHandler):    
    
    @log_errors
    def get(self,clip_id_val):
        clip_id = 0
        try:
            clip_id = int(clip_id_val)
        except:
            pass
        params = {}
        params['greeting'] = get_greeting()   
        params['user'] = users.get_current_user()
        clip = Clip.getClip(clip_id)
        params['clip'] = clip
        util.render("templates/detail.html", params, self.response)
        
class About(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        params = {}
        params['greeting'] = get_greeting()   
        params['user'] = users.get_current_user()
        util.render("templates/about.html", params, self.response)

        
class Delete(webapp.RequestHandler):    
    
    @log_errors
    @login_required
    def get(self,clip_id_val):
        clip_id = 0
        try:
            clip_id = int(clip_id_val)
        except:
            pass
        user = users.get_current_user()
        clip = Clip.getClip(clip_id)
        if clip and clip.user.user_id == user.user_id():
            clip.delete()
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        util.render("templates/deleted.html", params, self.response)        

class Test(webapp.RequestHandler):   
    
    def get(self):
        user = users.get_current_user()
        #Obrazky
        for i in range(1,2):
            src="http://img.aktualne.centrum.cz/334/18/3341852-ustavni-soud-v-brne.jpg";
            image = thumbnail(src)
            image.put()
            clip = Clip(page="http://www.somepage.com/",
                        type="null",
                        comment="null",
                        link="null",
                        src="http://behance.vo.llnwd.net/profiles/58035/projects/741714/bc8412ad79bd7ebd65a4c3c191f62ec9.jpg",
                        text="Testovaci text... blablabla bla bla",
                        user=UserInfo.getUserInfo(user))
            clip.image = image
            clip.put()
        #Linky
        for i in range(1,4):
            clip = Clip(page="http://www.somepage.com/",type="link",comment="komentar",link="http://www.google.com/",src="null",text="null",user=UserInfo.getUserInfo(user))
            clip.put()
        #Texty
        for i in range(1,4):
            clip = Clip(page="http://www.somepage.com/",
                        type="null",
                        comment="null",
                        link="null",src="null",
                        text="Testovaci text... blablabla bla bla",
                        user=UserInfo.getUserInfo(user))
            clip.put()
        #Obrazky
        for i in range(1,4):
            src="http://behance.vo.llnwd.net/profiles/58035/projects/741714/bc8412ad79bd7ebd65a4c3c191f62ec9.jpg";
            image = thumbnail(src)
            image.put()
            clip = Clip(page="http://www.somepage.com/",
                        type="null",
                        comment="null",
                        link="null",
                        src="http://behance.vo.llnwd.net/profiles/58035/projects/741714/bc8412ad79bd7ebd65a4c3c191f62ec9.jpg",
                        text="null",
                        user=UserInfo.getUserInfo(user))
            clip.image = image
            clip.put()

            
class ImageTest(webapp.RequestHandler):
    
    def get(self,src):
        src="http://behance.vo.llnwd.net/profiles/58035/projects/741714/bc8412ad79bd7ebd65a4c3c191f62ec9.jpg";
        image = thumbnail(src)
        image.put()
        
class Images(webapp.RequestHandler):
    
    @log_errors
    def get(self,type,name):
        image_type = str(type)
        image_name = str(name)
        if image_name.endswith(".jpg"):
            image_id = int(image_name[:-4]) 
            image = Image.getImage(image_id)
            if image:
                result = None
                if "tiny" == image_type:
                    result = image.tiny
                if "small" == image_type:
                    result = image.small
                util.renderJPEG(result, self.response)
        
        

class Post(webapp.RequestHandler):
    """
    Post the clip into system.
    """    
   
    @log_errors 
    def get(self):
        page = self.request.get('page')
        link = self.request.get('link')
        src = self.request.get('src')
        text = self.request.get('text')
        comment = self.request.get('comment') 
        user = oauth.get_current_user()
        if type and page and user:
            clip = Clip(page=page,type=type,comment=comment,link=link,src=src,text=text,user=UserInfo.getUserInfo(user))
            if src:
                image = thumbnail(src)
                clip.image = image
            clip.put()
                        

def get_greeting():
    user = users.get_current_user()
    if user:
        return ("Welcome, %s (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
    else:
        return ("<a href=\"%s\">Sign in</a>" % users.create_login_url("/"))   
            
        

