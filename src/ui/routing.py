'''
Created on Nov 14, 2010

@author: michalracek
'''

from dbo import UserInfo

def user_id(nick_or_id):
    """
    Finds user by the nickname or id.
    """
    user = UserInfo.getUserInfoByNick(nick_or_id)
    if not user:
        user =  UserInfo.getUserInfoById(nick_or_id)
    return user