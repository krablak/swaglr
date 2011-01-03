'''
Created on Dec 28, 2010

@author: michalracek

Handlers for swag reports used for sharing out of swagler.
'''

import util
import datetime
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import clips.api
import clips.likes.api
import ui.models
from ui.error_logging import log_errors
from util import handle_robots
from dbo import *
import dbo
import logging
import traceback
import StringIO
import urllib
import clips.validations 
import thirdparty.paging
import ui.routing
import clips.hashtag.api

PAGING = 20

class UserDay(webapp.RequestHandler):
    """
    Displays clips for given day and user.
    """
    
    @log_errors
    @handle_robots
    def get(self,user_id_val,date_val):
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id)
        #Prepare default page parameters
        params = ui.models.page_params()
        if user_info:
            user_id = user_info.user_id
            params['user_info'] = user_info
        #Read day date param value
        page_clips = []
        date_val = clips.validations.to_param(date_val)
        try:
            date = datetime.datetime.strptime(date_val,"%d-%m-%y")
            page_clips = Clip.getPageByUserAndDate(user_id,date)
            params['report_date'] = date
        except:
            logging.error("Cannot load clips for date from value %s" % (date_val))
        #Get today events
        params['day_clips'] = ui.models.to_united_clips(page_clips)
        util.render("templates/user_day_clips.html", params, self.response)
        
class UserDate(webapp.RequestHandler):
    """
    Displays clips for given day and user.
    """
    
    @log_errors
    @handle_robots
    def get(self,user_id_val,date_from_val,date_to_val):
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id)
        #Prepare default page parameters
        params = ui.models.page_params()
        if user_info:
            user_id = user_info.user_id
            params['user_info'] = user_info 
        #Read day date param value
        page_clips = []
        date_from_val = clips.validations.to_param(date_from_val)
        date_to_val = clips.validations.to_param(date_to_val)
        try:
            date_from = datetime.datetime.strptime(date_from_val,"%d-%m-%y")
            date_to = datetime.datetime.strptime(date_to_val,"%d-%m-%y")
            page_clips = Clip.getPageByUserAndDate(user_id,date_from,date_to)
            params['report_date'] = date_from
            params['report_date_to'] = date_to
        except:
            logging.error("Cannot load clips for date from value %s to %s" % (date_from,date_to))
        #Get today events
        params['day_clips'] = ui.models.to_united_clips(page_clips)
        util.render("templates/user_date_clips.html", params, self.response) 
        
        
class UserLikesDay(webapp.RequestHandler):
    """
    Displays liked clips for given day and user.
    """
    
    @log_errors
    @handle_robots
    def get(self,user_id_val,date_val):
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id)
        if user_info:
            user_id = user_info.user_id
        #Prepare default page parameters
        params = ui.models.page_params() 
        #Read day date param value
        page_clips = []
        date_val = clips.validations.to_param(date_val)
        try:
            date = datetime.datetime.strptime(date_val,"%d-%m-%y")
            page_clips = clips.likes.api.get_day_clips_by_user_likes(user_info, date)
            params['report_date'] = date
        except:
            logging.error("Cannot load clips for date from value %s" % (date_val))
        #Get today events
        params['day_clips'] = ui.models.to_united_clips(page_clips)
        util.render("templates/user_day_likes.html", params, self.response)
        
        
class UserLikesDate(webapp.RequestHandler):
    """
    Displays liked clips for given date and user.
    """
    
    @log_errors
    @handle_robots
    def get(self,user_id_val,date_from_val,date_to_val):
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id)
        if user_info:
            user_id = user_info.user_id
        #Prepare default page parameters
        params = ui.models.page_params() 
        #Read day date param value
        page_clips = []
        date_from_val = clips.validations.to_param(date_from_val)
        date_to_val = clips.validations.to_param(date_to_val)
        try:
            date_from = datetime.datetime.strptime(date_from_val,"%d-%m-%y")
            date_to = datetime.datetime.strptime(date_to_val,"%d-%m-%y")
            page_clips = clips.likes.api.get_day_clips_by_user_likes(user_info,date_from, date_to)
            params['report_date'] = date_from
            params['report_date_to'] = date_to
        except:
            logging.error("Cannot load clips for date from value %s to %s" % (date_from,date_to))
        #Get today events
        params['day_clips'] = ui.models.to_united_clips(page_clips)
        util.render("templates/user_date_likes.html", params, self.response)
        
        
class TaggedClips(webapp.RequestHandler):
    """
    Displays liked clips for given date and user.
    """
    
    @log_errors
    @handle_robots
    def get(self,tag_val,page_val):
        #Read page value
        page = clips.validations.to_int_param(page_val)
        #Get id or nick from request
        tag = urllib.unquote(clips.validations.to_param(tag_val))
        #Prepare default page parameters
        params = ui.models.page_params()
        page_clips = []
        tags_query = clips.hashtag.api.get_tag_query(tag)
        if tags_query:
            page_tags = ui.models.paging(params,tags_query,page,PAGING,url_prefix="swags/tagged/as/%s/page" % (tag))
            page_clips = clips.hashtag.api.get_clips_by_tags(page_tags)
        if tag:
            params['tag'] = tag[1:]
        params['day_clips'] = ui.models.to_day_clips(page_clips)
        util.render("templates/tag_clips.html", params, self.response)      

        
    



