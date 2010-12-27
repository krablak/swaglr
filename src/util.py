'''
Created on Feb 22, 2010

@author: michalracek
'''
from google.appengine.ext.webapp import template
import os
from google.appengine.ext import webapp
from django.utils import simplejson
from google.appengine.api import users, oauth

def render(path, values, response):
    response.headers['Content-Type'] = 'text/html'
    response.headers['Cache-Control'] = "public"
    path = os.path.join(os.path.dirname(__file__), path)
    response.out.write(template.render(path, values))
    
def execute_template(path, values):
    """
    Renders template and returns result as string.
    """
    path = os.path.join(os.path.dirname(__file__), path)
    return template.render(path, values)
    
def renderJPEG(image_data, response):
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Cache-Control'] = "public, max-age=315360000"
    response.out.write(image_data)
    
def renderJSON(values, response):
    """
    Renders given parameters as json response.
    """
    response.headers['Content-Type'] = 'application/json'
    response.out.write(simplejson.dumps(values))
    
    
html_escape_table = {
                     "&": "&amp;",
                     '"': "&quot;",
                     "'": "&apos;",
                     ">": "&gt;",
                     "<": "&lt;",
                     }
def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&quot;", "\"")
    s = s.replace("&apos;", "'")
    return s

def get_user():
    """
    Helper function to get currently logged user.
    """
    #Get logged user
    user = suppress_exeptions(users.get_current_user)
    if not user:
        #Try to get user from oauth
        user = suppress_exeptions(oauth.get_current_user)
    return user

def suppress_exeptions(function):
    """
    Helper function for hiding or exceptions. 
    Use it only when you really know what you are doing.
    """
    try:
        return function()
    except:
        return None
    
