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
            comment = str(self.request.get('comment'))
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
