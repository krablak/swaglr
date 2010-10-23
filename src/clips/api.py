'''
Created on Oct 15, 2010

Module defines interface for clips.

@author: michalracek
'''
from google.appengine.api import users
from google.appengine.api import oauth
import validations
from image import thumbnail
from dbo import Clip,UserInfo

class UserError(Exception):
    """
    Raised in case of error during user validation.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
    
def __validate_clip(page,link,src,text,comment):
    """
    Validates clip paramteres.
    """
    #Validate input values
    validations.validate_url(page,"page",True)
    #Check if one the required clip attributes is set.
    validations.is_one_set(link,src,text)
    if validations.is_set(link):
        validations.validate_url(link,"link",False)
    if validations.is_set(src):
        validations.validate_url(src,"src",False)
    #Validate text
    if validations.is_set(text):
        validations.validate_str(text,"text")
    #Validate comment
    validations.validate_str(comment,"comment")

PAGE = "page"
LINK = "link"
IMAGE = "image"
TEXT = "text" 
UNKNOWN = "unknown"
       
def __get_type(page,link,src,text):
    """
    Returns type by the clip parameter values.
    """
    if not validations.is_set(link) and not validations.is_set(src) and not validations.is_set(text):
        return PAGE
    if not validations.is_set(src) and validations.is_set(link):
        return LINK
    if validations.is_set(src):
        return IMAGE
    if validations.is_set(text):
        return TEXT
    return UNKNOWN

def store(page,link,src,text,comment):
    """
    Performs validation of passed values and stores clip into datastore. In case of invalid values throws
    exception.
    """
    #Check if user was provided by  google user api
    user = users.get_current_user()
    if not user:
        #Try to get user from oauth
        user = oauth.get_current_user()
        if not user:
            raise UserError("User is not logged in and clip cannot be stored into datastore.")
    __validate_clip(page,link,src,text,comment)
    #Prepare clip data object
    type = __get_type(page,link,src,text)
    #Create clip DO
    clip = Clip(type=type,page=page,comment=comment,link=link,src=src,text=text,user=UserInfo.getUserInfo(user))
    if src:
        image = thumbnail(src)
        clip.image = image
    clip.put()
    
def delete(id=0):
    """
    Deletes clip by id. Current user must be author of the deleted clip.
    """
    #Validate clip id
    validations.validate_int(id, "Clip id")
    #Get logged user
    user = users.get_current_user()
    if not user:
        #Try to get user from oauth
        user = oauth.get_current_user()
        if not user:
            raise UserError("User is not logged in and clip cannot be deleted from datastore.")
    #Get clip from datastore
    clip = Clip.getClip(id)
    #Check clip ownership
    if clip and clip.user.user_id == user.user_id():
        clip.delete()
    