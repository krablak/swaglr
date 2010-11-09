from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import pages
import ajax
import testpages


application = webapp.WSGIApplication([('/', pages.MainPage), 
                                      ('/post/', pages.Post), 
                                      ('/page/(.*)', pages.Paging),
                                      ('/user/(.*)/page/(.*)', pages.User),
                                      ('/clip/(.*)', pages.Detail),
                                      ('/api/clip/delete/', ajax.Delete),
                                      ('/api/clip/comment/', ajax.Comment),
                                      ('/api/clip/post/', ajax.Post),
                                      ('/about/', pages.About),
                                      #('/test/', testpages.Test),
                                      ('/images/(.*)/(.*)', pages.Images),
                                     ]
                                     , debug=True)

webapp.template.register_template_library('ui.templatefilters')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
