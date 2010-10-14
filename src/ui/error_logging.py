'''
Created on Oct 14, 2010

Module for logging of request errors.

@author: michalracek
'''
import logging
import traceback
import StringIO
import util
from google.appengine.api import users

logger = logging.getLogger()

def log_errors(handler_method):
    """
    A decorator handle raised exception, log it and display error page.
    """
    def execute(self, *args):
        try:
            handler_method(self, *args)
        except :
            #Get exception trace
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            #Get current user
            user_nick = "Unknown."
            if users.get_current_user():
                user_nick = users.get_current_user().nickname()
            #Log error
            logger.error("Error occured to user (%s) during request : (%s)" % (user_nick,message))
            util.render("templates/error.html", {}, self.response)
    return execute
