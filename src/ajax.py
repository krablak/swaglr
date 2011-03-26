'''
Created on Oct 22, 2010

@author: michalracek

AJAX API

'''

import swg_util
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from ui.error_logging import log_errors
import dbo
import logging
import traceback
import StringIO
from datetime import datetime

from dbo import *
import clips.api
import clips.validations 
import ui.models
import clips.likes.api
import clips.follow.api
import clips.hashtag.api




class Delete(webapp.RequestHandler):
    """
    Handler for ajax delete requests.
    """    
    
    @log_errors
    def post(self):
        clip_id = 0
        result = {}
        try:
            clip_id = int(self.request.get('id'))
            clips.api.delete(clip_id)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(simplejson.dumps(result))
        except Exception, inst:
            logging.error("Problem during clip delete.")
            self.error(500)
            
import ui.templatefilters
            
class Comment(webapp.RequestHandler):
    """
    Handler for ajax clip update requests.
    """    
    
    @log_errors
    def post(self):
        clip_id = 0
        result = {}
        try:
            clip_id = int(self.request.get('id'))
            comment = clips.validations.to_param(self.request.get('comment'),escape=False)
            clips.api.comment(clip_id, comment)
            clips.hashtag.api.update_hashtag_by_clip_id(clip_id)
            self.response.headers['Content-Type'] = 'text/html'
            result['comment'] = ui.templatefilters.to_tag_comment(comment)
            self.response.out.write(simplejson.dumps(result))
        except:
            #Get exception trace
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            logging.error("Problem during clip comment : %s" % (message))
            self.error(500)
            
class Post(webapp.RequestHandler):
    """
    Handler for clips posting.
    """    
    
    @log_errors
    def post(self):
        logging.debug("Posting clip start.")
        try:
            page = clips.validations.to_param(self.request.get('page'),escape=False)
            link = clips.validations.to_param(self.request.get('link'),escape=False)
            src = clips.validations.to_param(self.request.get('src'),escape=False)
            text = clips.validations.to_param(self.request.get('text'),escape=False)
            type = clips.validations.to_param(self.request.get('type'))
            comment = clips.validations.to_param(self.request.get('comment'),escape=False)
            title = clips.validations.to_param(self.request.get('title'),escape=False)
            logging.debug("page:'%s' comment:'%s'" % (page, comment))
            logging.debug("link:'%s' src:'%s'" % (link, src)) 
            clips.api.store(type, page, link, src, text, comment, title)
            logging.debug("Posted!")
            swg_util.renderJSON({'code' : 'OK', 'desc' : 'Clip posted.'}, self.response)
        except:
            #Get exception trace
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            logging.error("Problem during post : %s" % (message))
            swg_util.renderJSON({'code' : 'ERROR', 'desc' : "Clip post failed on error : %s" % (message)}, self.response)
        finally:
            logging.debug("Posting clip finished.") 
            
class Like(webapp.RequestHandler):
    """
    Handler for clip like.
    """    
    
    @log_errors
    def post(self):
        logging.debug("Like clip start.")
        try:
            clip_id = clips.validations.to_int_param(self.request.get('id'))
            logging.debug("Like clip id : %s" % clip_id)
            clips.likes.api.like(clip_id)
        finally:
            logging.debug("Like clip finised.")

class FollowSwitch(webapp.RequestHandler):
    """
    Handler for user follow/unfollow.
    """    
    
    @log_errors
    def post(self):
        logging.debug("User follow switch start.")
        try:
            #clips.follow.api
            user_id_val = clips.validations.to_param(self.request.get('user'))
            #Load user info by given parameter
            user_info = ui.routing.user_id(user_id_val)
            if user_info:
                logging.debug("User follow switch for user %s." % (user_id_val))    
                clips.follow.api.switch_follow(user_info)
        except:
            #Get exception trace
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            logging.error("Problem during user follow switch : %s" % (message))
            swg_util.renderJSON({'code' : 'ERROR', 'desc' : "User follow switch failed on error : %s" % (message)}, self.response)
        finally:
            logging.debug("User follow switch finished.")  
            

class HasNew(webapp.RequestHandler):
    """
    Handler checks if there are some new swags for logged users.
    """    
    
    @log_errors
    def post(self):
        logging.debug("HasNew clip start.")
        try:
            #Get params
            last_clip_id = str(self.request.get('id'))
            last_clip_date = str(self.request.get('date'))
            user = users.get_current_user()
            params = ui.models.page_params(req=self.request)
            new_clips_count = 0;
            if user and last_clip_id and last_clip_date:
                #Convert date string to date
                date = datetime.datetime.strptime(last_clip_date,"%y-%m-%d-%H-%M-%S")
                user_info = UserInfo.getUserInfo(user)
                new_clips = clips.follow.api.has_new_swag(user_info,date)
                swg_util.renderJSON({'code' : 'OK','count' : len(new_clips)}, self.response)
            else:
                swg_util.renderJSON({'code' : 'OK','count' : new_clips_count}, self.response)
        except:
            swg_util.renderJSON({'code' : 'ERROR','count' : 0}, self.response)
                 
        
