'''
Created on Aug 18, 2010

@author: michalracek
'''

import util
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import clips.api
import ui.models
from ui.error_logging import log_errors
from dbo import *
import dbo

PAGING = 20

class MainPage(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        #Get all events
        clips = Clip.getPage(0,PAGING)
        if len(clips)>PAGING:
            params['prev'] = "/page/%s" % (1)
            clips = clips[0:-1]
        params['day_clips'] = ui.models.to_day_clips(clips)
        params['json_clips'] = util.execute_template("templates/json/clips.json",{'clips' : clips})
        util.render("templates/index.html", params, self.response)
        
class Paging(webapp.RequestHandler):    
    
    @log_errors
    def get(self,page_val):
        page = 0    
        try:
            page = int(page_val)
        except:
            pass
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        #Get all events
        clips = Clip.getPage(page, PAGING)
        if len(clips)>PAGING:
            params['prev'] = "/page/%s" % (page+1)
            clips = clips[0:-1]
        if page>0:
            params['next'] = "/page/%s" % (page-1)            
        params['day_clips'] = ui.models.to_day_clips(clips)
        params['json_clips'] = util.execute_template("templates/json/clips.json",{'clips' : clips})
        util.render("templates/index.html", params, self.response)
        
class User(webapp.RequestHandler):    
    
    @log_errors
    def get(self,user_id_val,page_val):
        user_id = ""
        try:
            user_id = str(user_id_val)
        except:
            pass
        page = 0    
        try:
            page = int(page_val)
        except:
            pass
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        #Get all events
        clips = Clip.getPageByUser(page, PAGING, user_id)
        if len(clips)>PAGING:
            params['prev'] = "/user/%s/page/%s" % (user_id,page+1)
            clips = clips[0:-1]
        if page>0:
            params['next'] = "/user/%s/page/%s" % (user_id,page-1)            
        params['day_clips'] = ui.models.to_day_clips(clips)
        params['json_clips'] = util.execute_template("templates/json/clips.json",{'clips' : clips})
        util.render("templates/index.html", params, self.response)
        

        
class Detail(webapp.RequestHandler):    
    
    @log_errors
    def get(self,clip_id_val):
        clip_id = 0
        try:
            clip_id = int(clip_id_val)
        except:
            pass
        params = {}
        params['greeting'] = get_greeting()   
        params['user'] = users.get_current_user()
        clip = Clip.getClip(clip_id)
        params['clip'] = clip
        util.render("templates/detail.html", params, self.response)
        
class About(webapp.RequestHandler):    
    
    @log_errors
    def get(self):
        params = {}
        params['greeting'] = get_greeting()   
        params['user'] = users.get_current_user()
        util.render("templates/about.html", params, self.response)

        
class Delete(webapp.RequestHandler):    
    
    @log_errors
    @login_required
    def get(self,clip_id_val):
        clip_id = 0
        try:
            clip_id = int(clip_id_val)
        except:
            pass
        user = users.get_current_user()
        clip = Clip.getClip(clip_id)
        if clip and clip.user.user_id == user.user_id():
            clip.delete()
        params = {}
        params['greeting'] = get_greeting()
        params['user'] = users.get_current_user()
        util.render("templates/deleted.html", params, self.response)        

class Test(webapp.RequestHandler):   
    
    @login_required
    def get(self):
        #Texty
        clips.api.store("http://behance.vo.llnwd.net/", "null", "null", "Lorem ipsum kasd facete reformidans ne sed, mea etiam simul forensibus ad. Cum tempor intellegat intellegam an. Qui congue nonummy.", "Et sit molestie delicatissimi. Sit te impedit adipisci. His eu prompta eleifend sententiae. Sed ut modus tation, id dicant aliquyam vulputate has, in laudem feugiat necessitatibus eam.")
        clips.api.store("http://www.google.com/", "null", "null", "Eum ex mazim harum assentior. Eum recteque dissentiunt et. Usu possit conclusionemque te. Et usu.", "null")
        clips.api.store("http://www.climbing.com/", "null", "null", "Ad postulant efficiantur eam.", "null")
        clips.api.store("http://www.somepage.com/", "null", "http://webdesignledger.com/wp-content/uploads/2010/10/high_quality_fonts.jpg", "null", "Paulo commune periculis vel cu, vel ne zzril oblique volumus. Sint fuisset ea eam. Ut sit audiam pertinax. Eam at kasd ipsum.")
        clips.api.store("http://behance.vo.llnwd.net/", "http://www.somepage.com/linked/link", "null", "null" , "In his sumo nonumy iracundia. Per ignota imperdiet et. Id qui eruditi alienum, in pri vidisse aliquando, pri in duis nostrum. Vim ornatus alienum at. Mea utinam tempor cu, choro qualisque ne vim, eruditi perpetua forensibus sed ut.")
        clips.api.store("http://www.webdesigns.com/", "null", "null", "Cum nusquam antiopam sententiae te, eu tale nominati evertitur sea. Ius prompta torquatos et. Cu ius.", "Veniam petentium at per, latine virtute invenire eum ad, augue eripuit definiebas no. His cu epicurei voluptatum efficiantur. Admodum scaevola vix eu. An usu homero pericula, mei ut ignota salutandi ludus.")
        clips.api.store("http://www.webdesigns.com/", "null", "null", "In clita pericula usu, impetus eruditi salutatus ad est, id vel probo illum. Usu ea exerci similique, mutat apeirian est eu. Duis ponderum eos ex, ei mea offendit indoctum. Ad aliquip apeirian conceptam qui, accumsan consequuntur mei ei.", "null")
        #Obrazky
        for i in range(1,2):
            clips.api.store("http://behance.vo.llnwd.net/", "null", "http://img.aktualne.centrum.cz/334/18/3341852-ustavni-soud-v-brne.jpg", "null" , "null")
        #Linky
        clips.api.store("http://behance.vo.llnwd.net/", "http://www.somepage.com/linked/link", "null", "null" , "Ne iusto sensibus maluisset cum. Tamquam equidem nam ut, copiosae concludaturque ne pri, aliquip tibique cum ea. His et solet phaedrum, liber democritum reformidans duo in. Eu eos hinc aliquyam. Ex nominavi rationibus sit, stet audire ius ad, ea pro.")
        clips.api.store("http://twitter.com/", "http://http://twitter.com/krablak/", "null", "null" , " Ei quo graece impetus complectitur. Odio laudem.")
        clips.api.store("http://www.somepage.com/", "null", "http://s3.buysellads.com/1243129/39717-1287502970.jpg", "null", " His cu epicurei voluptatum efficiantur. Admodum scaevola vix eu. An usu homero pericula, mei ut ignota salutandi ludus.Paulo commune periculis vel cu, vel ne zzril oblique volumus. Sint fuisset ea eam. Ut sit audiam pertinax. Eam at kasd ipsum.")
        clips.api.store("http://behance.vo.llnwd.net/", "http://www.somepage.com/linked/link", "null", "null" , "No decore offendit conclusionemque vim, mea discere utroque gubergren no. Vim et habeo mediocrem assentior. Ne accumsan indoctum sit. Cu vel blandit facilisi, eum alii animal consequat ea, ad his noluisse cotidieque efficiantur.")
        
        for i in range(1,2):
            clips.api.store("http://behance.vo.llnwd.net/", "null", "http://img.aktualne.centrum.cz/334/18/3341852-ustavni-soud-v-brne.jpg", "null" , "Komentar k obrazku.")
        #Obrazky
        clips.api.store("http://www.somepage.com/", "null", "http://behance.vo.llnwd.net/profiles/58035/projects/741714/bc8412ad79bd7ebd65a4c3c191f62ec9.jpg", "null", "Paulo commune periculis vel cu, vel ne zzril oblique volumus. Sint fuisset ea eam. Ut sit audiam pertinax. Eam at kasd ipsum.")
        clips.api.store("http://www.somepage.com/", "null", "http://webdesignledger.com/wp-content/uploads/2010/10/high_quality_fonts.jpg", "null", "Paulo commune periculis vel cu, vel ne zzril oblique volumus. Sint fuisset ea eam. Ut sit audiam pertinax. Eam at kasd ipsum.")
        clips.api.store("http://www.climbing.com/", "null", "null", "Ad postulant efficiantur eam.", "null")
        
class Images(webapp.RequestHandler):
    """
    Finds image in datastore and returns it as response.
    """
    
    @log_errors
    def get(self,type,name):
        image_type = str(type)
        image_name = str(name)
        if image_name.endswith(".jpg"):
            image_id = int(image_name[:-4]) 
            image = Image.getImage(image_id)
            if image:
                result = None
                if "tiny" == image_type:
                    result = image.tiny
                if "small" == image_type:
                    result = image.small
                util.renderJPEG(result, self.response)
        
        

class Post(webapp.RequestHandler):
    """
    Post the clip into system.
    """    
   
    @log_errors 
    def get(self):
        page = self.request.get('page')
        link = self.request.get('link')
        src = self.request.get('src')
        text = self.request.get('text')
        comment = self.request.get('comment') 
        clips.api.store(page, link, src, text, comment)
                       

def get_greeting():
    user = users.get_current_user()
    if user:
        return ("Welcome, %s (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
    else:
        return ("<a href=\"%s\">Sign in</a>" % users.create_login_url("/"))   
            
        

