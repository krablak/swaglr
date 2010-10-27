from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import pages
import ajax


application = webapp.WSGIApplication([('/', pages.MainPage), 
                                      ('/post/', pages.Post), 
                                      ('/page/(.*)', pages.Paging),
                                      ('/user/(.*)/page/(.*)', pages.User),
                                      ('/clip/(.*)', pages.Detail),
                                      ('/api/clip/delete/', ajax.Delete),
                                      ('/api/clip/comment/', ajax.Comment),
                                      ('/about/', pages.About),
                                      ('/images/(.*)/(.*)', pages.Images),
                                     ]
                                     , debug=True)

webapp.template.register_template_library('ui.templatefilters')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
