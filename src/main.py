from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import pages
import ajax
import testpages


application = webapp.WSGIApplication([('/', pages.MainPage), 
                                      ('/page/(.*)', pages.Paging),
                                      ('/user/(.*)/page/(.*)', pages.User),
                                      ('/swag/(.*)', pages.Detail),
                                      ('/api/clip/delete/', ajax.Delete),
                                      ('/api/clip/comment/', ajax.Comment),
                                      ('/api/clip/post/', ajax.Post),
                                      ('/api/clip/like/', ajax.Like),
                                      #('/test/', testpages.Test),
                                      ('/images/(.*)/(.*)', pages.Images),
                                     ]
                                     , debug=True)

webapp.template.register_template_library('ui.templatefilters')
webapp.template.register_template_library('ui.embedfilters')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
