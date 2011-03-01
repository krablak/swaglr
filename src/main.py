import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import pages
import ajax
import reports


application = webapp.WSGIApplication([('/', pages.MainPage), 
                                      ('/page/(.*)', pages.Paging),
                                      ('/user/(.*)/page/(.*)', pages.User),
                                      ('/swag/(.*)', pages.Detail),
                                      ('/swag/(.*)', pages.Detail),
                                      ('/swags/all/page/(.*)', pages.AllPage),
                                      ('/swags/popular/', pages.Popular),
                                      ('/swags/liked/by/(.*)/page/(.*)', pages.LikedByCurrentUser),
                                      ('/swags/share/', pages.Share),
                                      ('/swags/by/(.*)/on/(.*)', reports.UserDay),
                                      ('/swags/by/(.*)/from/(.*)/to/(.*)', reports.UserDate),
                                      ('/swags/liked/by/(.*)/from/(.*)/to/(.*)', reports.UserLikesDate),
                                      ('/swags/liked/by/(.*)/on/(.*)', reports.UserLikesDay),
                                      ('/swags/tagged/as/(.*)/page/(.*)', reports.TaggedClips),
                                      ('/web-api/clip/post/', pages.WebPost),
                                      ('/api/clip/comment/', ajax.Comment),
                                      ('/api/clip/post/', ajax.Post),
                                      ('/api/clip/like/', ajax.Like),
                                      ('/api/clip/delete/', ajax.Delete),
                                      ('/api/user/switch_follow/', ajax.FollowSwitch),
                                      ('/images/(.*)/(.*)', pages.Images),
                                     ]
                                     , debug=True)

webapp.template.register_template_library('ui.templatefilters')
webapp.template.register_template_library('ui.embedfilters')
webapp.template.register_template_library('ui.componentfilters')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
