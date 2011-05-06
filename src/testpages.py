'''
Created on Nov 2, 2010

@author: michalracek
'''
import swg_util
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
from clips.hashtag.hashtag_dbo import HashTags 
from google.appengine.api import taskqueue
import clips.validations
import thirdparty.paging

       
            
class UpdateTagsWorker(webapp.RequestHandler):   
    
    
    def get(self,page_val):
        #Read page value
        page = clips.validations.to_int_param(page_val)
        page_query = thirdparty.paging.PagedQuery(HashTags.all(),50)
        hashtags = page_query.fetch_page(page)
        result = ""
        for hashtag in hashtags:
            lowertags = []
            for tag in hashtag.tags:
                lowertags.append(tag.lower())
            hashtag.tags = lowertags;
            result = "%s<br>clip: (%s) tags:(%s)" % (result,hashtag.key().id(),str(lowertags)) 
            hashtag.put();
            
        self.response.out.write(result)
            
            




