'''
Created on Oct 22, 2010

@author: michalracek

AJAX API

'''

import util
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import clips.api
import clips.validations 
import ui.models
from ui.error_logging import log_errors
from dbo import *
import dbo
import logging
import traceback
import StringIO



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
            comment = clips.validations.to_param(self.request.get('comment'))
            clips.api.comment(clip_id, comment)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(simplejson.dumps(result))
        except:
            #Get exception trace
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            logging.error("Problem during clip comment : %s" % (message) )
            self.error(500)
            
class Post(webapp.RequestHandler):
    """
    Handler for clips posting.
    """    
    
    @log_errors
    def post(self):
        logging.debug("Posting clip start.")
        try:
            page = clips.validations.to_param(self.request.get('page'))
            link = clips.validations.to_param(self.request.get('link'))
            src = clips.validations.to_param(self.request.get('src'))
            text = clips.validations.to_param(self.request.get('text'))
            comment = clips.validations.to_param(self.request.get('comment'))
            logging.debug("page:'%s' comment:'%s'" % (page,comment))
            logging.debug("link:'%s' src:'%s'" % (link,src)) 
            clips.api.store(page, link, src, text, comment)
            logging.debug("Posted!")
        except:
            #Get exception trace
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            logging.error("Problem during post : %s" % (message) )
            self.error(500)
        finally:
           logging.debug("Posting clip finised.") 
