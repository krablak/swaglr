'''
Created on Nov 2, 2010

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
from clips.follow.follow_dbo import FollowedUsers,Followers 

class UpdateFollows(webapp.RequestHandler):   
    
    @login_required
    def get(self):
        users = UserInfo.all().fetch(limit=100)
        for user in users:
            FollowedUsers.get_follow_setting(user)
            
class UpdateUsers(webapp.RequestHandler):   
    
    @login_required
    def get(self,user_id_val):
        #Get id or nick from request
        user_id = clips.validations.to_param(user_id_val)
        #Load user info by given parameter
        user_info = ui.routing.user_id(user_id)
        if user_info:
            logging.debug("Starting follow updates for user %s " % (user_info.nick))
            found_clips = Clip.all().filter("user =", user_info).fetch(limit=5000)
            for clip in found_clips:
                #Get follow settings for current user
                follow_settings = FollowedUsers.get_follow_setting(user_info)
                #Create clip followers
                clip_followers = Followers.get_by_clip(clip)
                if not clip_followers:
                    clip_followers = Followers(parent=clip)
                    clip_followers.users = follow_settings.followed_users
                    clip_followers.users.append(user_info.key())
                    clip_followers.order_date = clip.date
                    clip_followers.put()
                else:
                    clip_followers[0].order_date = clip.date
                    clip_followers[0].put() 
            logging.debug("Finished follow updates for user %s " % (user_info.nick))
        else:
            logging.debug("No user found for nick %s " % (user_id))
            
            




