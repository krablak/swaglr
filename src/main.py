from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from pages import *


application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/post/', Post), 
                                      ('/page/(.*)', Paging),
                                      ('/user/(.*)/page/(.*)', User),
                                      ('/clip/(.*)', Detail),
                                      ('/delete/(.*)', Delete),
                                      ('/about/', About),
                                      ('/images/(.*)/(.*)', Images),
                                      ('/test/', Test),
                                     ]
                                     , debug=True)

webapp.template.register_template_library('ui.templatefilters')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
