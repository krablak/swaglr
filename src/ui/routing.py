'''
Created on Nov 14, 2010

@author: michalracek
'''

import urllib

from dbo import UserInfo

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