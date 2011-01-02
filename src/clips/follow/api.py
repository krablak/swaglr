'''
Created on Dec 13, 2010

@author: michalracek

Provides all functionality required for following

'''
from dbo import UserInfo,Clip
from follow_dbo import FollowedUsers,Followers
from google.appengine.api import users
import util


def switch_follow(follow_user_info):
    """
    follows or unfollows user passed as argument.
    """
    if is_followed(follow_user_info):
        unfollow(follow_user_info)
    else:
        follow(follow_user_info)

def follow(follow_user_info):
    """
    Follow user by nick or id
    """
    user = util.get_user()
    #Follow could be done only for
    if user:
        #Get current user info
        user_info = UserInfo.getUserInfo(user)
        #Get follow settings for current user
        follow_settings = FollowedUsers.get_follow_setting(follow_user_info)
        #Add new user to follow settings
        follow_settings.followed_users.append(user_info.key())
        follow_settings.put()
        #Add followed user to some latest clips
        __update_followed_clips(follow_user_info, user_info, True)


def unfollow(unfollow_user_info):
    """
    Follow user by nick or id
    """
    user = util.get_user()
    #Follow could be done only for
    if user:
        #Get current user info
        user_info = UserInfo.getUserInfo(user)
        #Get follow settings for current user
        follow_settings = FollowedUsers.get_follow_setting(unfollow_user_info)
        #Remove from followed users 
        follow_settings.followed_users.remove(user_info.key())
        follow_settings.put()
        #Remove unfollowed user from clips
        __update_followed_clips(unfollow_user_info, user_info, False)
        
def is_followed(follow_user_info):
    """
    Checks if passed user is followed by the current user.
    """
    user = util.get_user()
    #Follow could be done only for
    if user and follow_user_info:
        #Get current user info
        user_info = UserInfo.getUserInfo(user)
        #Get follow settings for passed user
        follow_settings = FollowedUsers.get_follow_setting(follow_user_info)
        if follow_settings and follow_settings.followed_users and user_info.key() in follow_settings.followed_users:
            return True
        return False
    

def __update_followed_clips(followed_user_info,current_user_info,add):
    """
    Adds current user as follower to last X followed clips.
    """
    #Get some  of followed user last clips
    clips =  Clip.getPageByUserInfoQuery(followed_user_info).fetch(3)
    #Add current user as new follower of this clip.
    for clip in clips:
        followers = Followers.get_by_clip(clip)
        if followers:
            if add:
                followers[0].users.append(current_user_info.key())
            else:
                followers[0].users.remove(current_user_info.key())
            followers[0].put()
        
        
def on_clip_created(clip):
    """
    Should be called after clip storing into DS. Followers information will be added to clip.
    """
    user = util.get_user()
    #Follow could be done only for
    if user:
        #Get current user info
        user_info = UserInfo.getUserInfo(user)
        #Get follow settings for current user
        follow_settings = FollowedUsers.get_follow_setting(user_info)
        #Create clip followers
        clip_followers = Followers(parent=clip)
        clip_followers.users = follow_settings.followed_users
        clip_followers.users.append(user_info.key())
        clip_followers.put()
        
def on_clip_delete(clip):
    """
    Should be called when clip is deleted.
    """
    if clip:
        Followers.delete_by_clip(clip)        


def get_followers_query(user_info):
    """
    Returns query for finding clip follower containing given user info.
    Should be used to get query for paging purposes.
    """
    if not user_info:
        user = util.get_user()
        if user:
            user_info = UserInfo.getUserInfo(user)
    if user_info:
        return Followers.all().filter("users =",user_info.key()).order("-order_date")
    
def get_clips_by_followers(followers_keys):
    if followers_keys:
        clip_keys = [ key.parent().key() for key in followers_keys]
        return Clip.get(clip_keys)
