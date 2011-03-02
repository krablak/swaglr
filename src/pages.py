'''
Created on Aug 18, 2010

@author: michalracek
'''

import swg_util
import datetime
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import clips.api
import clips.likes.api
import ui.models
from ui.error_logging import log_errors
from dbo import *
import dbo
import logging
import traceback
import StringIO
import clips.validations 
import thirdparty.paging
import ui.routing

PAGING = 20

class MainPage(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        user = users.get_current_user()
        params = ui.models.page_params(req=self.request)
        if user:
            user_info = UserInfo.getUserInfo(user)
            follow_query = clips.follow.api.get_followers_query(user_info)
            page_followers = ui.models.paging(params,follow_query,0,PAGING)
            page_clips = clips.follow.api.get_clips_by_followers(page_followers)
            params['day_clips'] = ui.models.to_day_clips(page_clips)
            swg_util.render("templates/index.html", params, self.response)
        else:
            #Get paging content
            page_clips = ui.models.paging(params,Clip.getPagingQuery(),0,PAGING) 
            params['day_clips'] = ui.models.to_day_clips(page_clips)
            swg_util.render("templates/index.html", params, self.response)
            
            
class AllPage(webapp.RequestHandler):    
    
    @log_errors
    def get(self,page_val):
        params = ui.models.page_params(req=self.request)
        #Read page value
        page = clips.validations.to_int_param(page_val)
        #Get paging content
        page_clips = ui.models.paging(params,Clip.getPagingQuery(),page,PAGING,url_prefix="swags/all/page") 
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        swg_util.render("templates/all.html", params, self.response)
        
class Popular(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        params = ui.models.page_params(req=self.request)
        #Get paging content
        page_clips = clips.likes.api.get_popular_clips(clips_count=20)
        params['day_clips'] = ui.models.to_united_clips(page_clips)
        swg_util.render("templates/popular.html", params, self.response)
        
class LikedByCurrentUser(webapp.RequestHandler):    
    
    @log_errors
    def get(self,user_id_val,page_val):
        params = ui.models.page_params(req=self.request)
        page_clips = []
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id)
        if user_info:
            #Read page value
            page = clips.validations.to_int_param(page_val)
            #Get paged user likes
            user_likes = ui.models.paging(params,clips.likes.api.get_liked_by_query(user_info),page,PAGING,url_prefix="swags/liked/by/%s/page" % (user_info.nick))
            #Get clips by user likes
            found_clips = clips.likes.api.get_clips_by_user_likes(user_likes)
            page_clips = ui.models.to_united_clips(found_clips)
        params['day_clips'] = page_clips 
        swg_util.render("templates/liked.html", params, self.response)
        
class Paging(webapp.RequestHandler):    
    
    @log_errors
    def get(self,page_val):
        #Read page value
        page = clips.validations.to_int_param(page_val)
        #get user and check if only followed clips should be displayed.
        user = users.get_current_user()
        params = ui.models.page_params(req=self.request)
        if user:
            user_info = UserInfo.getUserInfo(user)
            follow_query = clips.follow.api.get_followers_query(user_info)
            page_followers = ui.models.paging(params,follow_query,page,PAGING)
            page_clips = clips.follow.api.get_clips_by_followers(page_followers)
            params['day_clips'] = ui.models.to_day_clips(page_clips)
            swg_util.render("templates/index.html", params, self.response)
        else:
            #Get all events
            page_clips = ui.models.paging(params,Clip.getPagingQuery(),page,PAGING) 
            params['day_clips'] = ui.models.to_day_clips(page_clips)
            swg_util.render("templates/index.html", params, self.response)

class User(webapp.RequestHandler):    
    
    @log_errors
    def get(self,user_id_val,page_val):
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id_val)
        if user_info:
            user_id = user_info.user_id 
        #Read page value
        page = clips.validations.to_int_param(page_val)
        params = ui.models.page_params(req=self.request)
        #Set displayed user
        params['detail_user_info'] = user_info
        #Get all events
        page_clips = ui.models.paging(params,Clip.getPageByUserQuery(user_id=user_id),page,PAGING,user_id)
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        swg_util.render("templates/user.html", params, self.response)
        

        
class Detail(webapp.RequestHandler):    
    
    @log_errors
    def get(self,clip_id_val):
        clip_id = clips.validations.to_int_param(clip_id_val)
        params = ui.models.page_params(req=self.request)
        #Current clip
        clip = Clip.getClip(clip_id)
        params['clip'] = clip
        #Add likers to clip details
        if clip:
            params['likers'] = clips.likes.api.get_user_likes_by_clip(clip)
        #Get use events events
        clips_query = Clip.getPageByUserQuery(user_id=clip.user.user_id)
        if clips_query:
            page_clips = ui.models.paging(params,clips_query,0,PAGING,clip.user.nick)
            params['day_clips'] = ui.models.to_day_clips(page_clips)
        else:
            params['day_clips'] = []
        swg_util.render("templates/detail.html", params, self.response)

        
class Delete(webapp.RequestHandler):    
    
    @log_errors
    @login_required
    def get(self,clip_id_val):
        clip_id = clips.validations.to_int_param(clip_id_val)
        user = users.get_current_user()
        clip = Clip.getClip(clip_id)
        if clip and clip.user.user_id == user.user_id():
            clip.delete()
        params = ui.models.page_params(req=self.request)
        swg_util.render("templates/deleted.html", params, self.response)        


class Share(webapp.RequestHandler):    
    
    @log_errors
    @login_required
    def get(self):
        params = ui.models.page_params(req=self.request)
        params['today_date'] = datetime.datetime.now()
        params['before_date'] = datetime.datetime.now() - datetime.timedelta(days=7)
        swg_util.render("templates/share.html", params, self.response)


       
class Images(webapp.RequestHandler):
    """
    Finds image in datastore and returns it as response.
    """
    
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
                swg_util.renderJPEG(result, self.response)
                
                
import urllib        
        
class WebPost(webapp.RequestHandler):    
    
    @log_errors
    def get(self):        
        user = users.get_current_user()
        if user:
            swg_util.render("templates/post/webpost.html", {}, self.response)
        else:
            self.redirect(users.create_login_url("/web-api/clip/post/"))
            
    def post(self):
        logging.debug("Posting clip start.")
        user = users.get_current_user()
        if user:        
            try:
                page = clips.validations.to_param(self.request.get('page'))
                link = clips.validations.to_param(self.request.get('link'))
                src = clips.validations.to_param(self.request.get('src'))
                text = clips.validations.to_param(self.request.get('text'))
                type = clips.validations.to_param(self.request.get('type'))
                comment = clips.validations.to_param(self.request.get('comment'))
                title = clips.validations.to_param(self.request.get('title'))
                logging.debug("page:'%s' comment:'%s'" % (page, comment))
                logging.debug("link:'%s' src:'%s'" % (link, src)) 
                clips.api.store(type, page, link, src, text, comment, title)
                logging.debug("Posted!")
            except:
                #Get exception trace
                fp = StringIO.StringIO()
                traceback.print_exc(file=fp)
                message = fp.getvalue()
                logging.error("Problem during post : %s" % (message))
            finally:
                logging.debug("Posting clip finished.")
        else:
            logging.debug("User was not logged in and clip post was canceled.")
        swg_util.render("templates/post/posted.html", {}, self.response)
   
            
        

