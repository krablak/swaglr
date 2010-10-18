'''
Created on Feb 22, 2010

@author: michalracek
'''
from google.appengine.ext.webapp import template
import os
from google.appengine.ext import webapp

def render(path, values, response):
    response.headers['Content-Type'] = 'text/html'
    path = os.path.join(os.path.dirname(__file__), path)
    response.out.write(template.render(path, values))
    
def execute_template(path, values):
    """
    Renders template and returns result as string.
    """
    path = os.path.join(os.path.dirname(__file__), path)
    return template.render(path, values)

def renderjson(path, values, response):
    response.headers['Content-Type'] = 'application/json'
    path = os.path.join(os.path.dirname(__file__), path)
    response.out.write(template.render(path, values))
    
def renderJPEG(image_data, response):
    response.headers['Content-Type'] = 'image/jpeg'
    response.out.write(image_data)
    
    
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


    
