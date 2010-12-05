'''
Created on Oct 15, 2010

Module defines interface for clips.

@author: michalracek
'''
from google.appengine.api import users,oauth
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
    
def __get_user():
    """
    Helper function to get currently logged user.
    """
    #Get logged user
    user = users.get_current_user()
    if not user:
        #Try to get user from oauth
        user = oauth.get_current_user()
        if not user:
            raise UserError("User is not logged in and clip cannot be deleted from datastore.")
    return user

PAGE = "PAGE"
LINK = "LINK"
IMAGE = "IMAGE"
TEXT = "TEXT" 
UNKNOWN = "UNKNOWN"
       
def __validate_by_type(type,page,link,src,text,title):
    """
    Validates clip values according to type.
    """
    #Validate clip type
    validations.validate_str(type,"Type")
    #Validate if type match to allowed clip types
    validations.is_one_of_them(type,[PAGE,LINK,IMAGE,TEXT])    
    #Validate if required value is set
    validations.validate_str(page,"Page")
    #Convert optional title param
    title = validations.to_param(title)
    #Check values according to defined type
    if type == PAGE:
        pass
    if type == LINK:
        validations.validate_str(link,"Link")
        validations.validate_null(text,"text for LINK clip type.")
        validations.validate_null(src,"src for LINK clip type.")
    if type == IMAGE:
        validations.validate_str(src,"Src")
        validations.validate_null(text,"text for IMAGE clip type.")
        validations.validate_null(text,"text for IMAGE clip type.")
        validations.validate_null(link,"link for IMAGE clip type.")
    if type == TEXT:  
        validations.validate_str(text,"Text")
        validations.validate_null(src,"src for TEXT clip type.")
        validations.validate_null(link,"link for TEXT clip type.")

def store(type,page,link,src,text,comment,title):
    """
    Performs validation of passed values and stores clip into datastore. In case of invalid values throws
    exception.
    """
    #Check if user was provided by  google user api
    user = __get_user()
    #Check if clip type is set
    validations.is_set(type);
    
    #Check clip data object
    __validate_by_type(type,page,link,src,text,title)
    #Create clip DO
    clip = Clip(type=type,page=page,comment=comment,link=link,src=src,text=text,user=UserInfo.getUserInfo(user),title=title,likes=0)
    if src:
        image = thumbnail(src)
        clip.image = image
    clip.put()
    return clip
    
def delete(id=0):
    """
    Deletes clip by id. Current user must be author of the deleted clip.
    """
    #Get logged user
    user = __get_user()
    #Validate clip id
    validations.validate_int(id, "Clip id")
    #Get clip from datastore
    clip = Clip.getClip(id)
    #Check clip ownership
    if clip and clip.user.user_id == user.user_id():
        clip.delete()
        
def comment(id=0,comment=""):
    """
    Adds or update comment to clip found by clip id.
    """
    #Get logged user
    user = __get_user()
    #Validate clip id
    validations.validate_int(id, "Clip id")
    #Validate comment
    comment = validations.to_param(comment)
    #Get clip from datastore
    clip = Clip.getClip(id)
    #Check clip ownership
    if clip and clip.user.user_id == user.user_id():
        clip.comment = comment
        clip.put()
    return clip
    
    
    