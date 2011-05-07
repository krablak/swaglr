'''
Created on Nov 14, 2010

@author: michalracek
'''

import urllib
import inspect

from dbo import UserInfo


def fill_page_arg(handler_method):
    """
    A decorator for handlers which requires page argument but this argument is not given.
    """
    def execute(self, *args):
        #Get defined argument for called function
        def_args = inspect.getargspec(handler_method);
        #Check if page val is defined
        if len(def_args[0]) > (len(args)+1):
            updated_args = []
            for old_arg in args:
                updated_args.append(old_arg)                                   
            updated_args.append(0)
            handler_method(self, *updated_args)
        else:      
            handler_method(self, *args)
    return execute

def user_id(nick_or_id):
    """
    Finds user by the nickname or id.
    """
    #Decode nick from URL format
    nick_or_id_val = urllib.unquote(nick_or_id)
    user = UserInfo.getUserInfoByNick(nick_or_id_val)
    if not user:
        user =  UserInfo.getUserInfoById(nick_or_id_val)
    if len(user)>0:
        return user[0]