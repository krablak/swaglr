'''
Created on Aug 18, 2010

@author: michalracek
'''

import util
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import clips.api
import ui.models
from ui.error_logging import log_errors
from dbo import *
import dbo
import logging
import traceback
import StringIO
import clips.validations 

PAGING = 20

class MainPage(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        params = ui.models.page_params()
        #Get all events
        page_clips = Clip.getPage(0,PAGING)
        ui.models.paging(params,page_clips,0,PAGING) 
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        util.render("templates/index.html", params, self.response)
        
class Paging(webapp.RequestHandler):    
    
    @log_errors
    def get(self,page_val):
        #Read page value
        page = clips.validations.to_int_param(page_val)
        params = ui.models.page_params()
        #Get all events
        page_clips = Clip.getPage(page, PAGING)
        ui.models.paging(params,page_clips,page,PAGING)            
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        util.render("templates/index.html", params, self.response)

import ui.routing

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
        params = ui.models.page_params()
        #Get all events
        page_clips = Clip.getPageByUser(page, PAGING, user_id)
        ui.models.paging(params,page_clips,page,PAGING,user_id)          
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        util.render("templates/index.html", params, self.response)
        

        
class Detail(webapp.RequestHandler):    
    
    @log_errors
    def get(self,clip_id_val):
        clip_id = clips.validations.to_int_param(clip_id_val)
        params = ui.models.page_params()
        #Current clip
        clip = Clip.getClip(clip_id)
        params['clip'] = clip
        #Get all events
        page_clips = Clip.getPageByUser(0, PAGING, clip.user.user_id)
        ui.models.paging(params,page_clips,0,PAGING,clip.user.user_id) 
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        util.render("templates/detail.html", params, self.response)

        
class Delete(webapp.RequestHandler):    
    
    @log_errors
    @login_required
    def get(self,clip_id_val):
        clip_id = clips.validations.to_int_param(clip_id_val)
        user = users.get_current_user()
        clip = Clip.getClip(clip_id)
        if clip and clip.user.user_id == user.user_id():
            clip.delete()
        params = ui.models.page_params()
        util.render("templates/deleted.html", params, self.response)        

        
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
                util.renderJPEG(result, self.response)
                       
   
            
        

