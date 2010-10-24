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



class Delete(webapp.RequestHandler):
    """
    Handler for ajax delete requests.
    """    
    
    @log_errors
    def post(self,clip_id_val):
        clip_id = 0
        result = {}
        try:
            clip_id = int(clip_id_val)
            clips.api.delete(clip_id)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(simplejson.dumps(result))
        except Exception, inst:
            logging.error("Problem during clip delete.")
            self.error(500)
