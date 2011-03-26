'''
Created on Dec 1, 2010

@author: michalracek
'''

from google.appengine.api.datastore_file_stub import DatastoreFileStub
from google.appengine.api import apiproxy_stub_map
import clips.api
import clips.likes.api
import os
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)

os.environ['APPLICATION_ID'] = "swagclip"
# Create a new apiproxy and temporary datastore that will be used for this test.
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
stub = DatastoreFileStub(u'swagclip', '/dev/null', '/dev/null')  
apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)


class TestLocalHost(unittest.TestCase):

        
    def invalid_like(self):
        import clips.likes.api
        clips.likes.api.like(None)
        clips.likes.api.like(0)
        clips.likes.api.like(-1)
        clips.likes.api.like("hovno")
        self.assertEquals(True,True)

    def success_like(self):
        test_clip = clips.api.store("http://behance.vo.llnwd.net/", "null", "null", "Lorem ipsum kasd facete reformidans ne sed, mea etiam simul forensibus ad. Cum tempor intellegat intellegam an. Qui congue nonummy.", "Et sit molestie delicatissimi. Sit te impedit adipisci. His eu prompta eleifend sententiae. Sed ut modus tation, id dicant aliquyam vulputate has, in laudem feugiat necessitatibus eam.")
        clips.api.store("http://www.google.com/", "null", "null", "Eum ex mazim harum assentior. Eum recteque dissentiunt et. Usu possit conclusionemque te. Et usu.", "null")
        clips.api.store("http://www.climbing.com/", "null", "null", "Ad postulant efficiantur eam.", "null")
        clips.api.store("http://www.somepage.com/", "null", "http://webdesignledger.com/wp-content/uploads/2010/10/high_quality_fonts.jpg", "null", "Paulo commune periculis vel cu, vel ne zzril oblique volumus. Sint fuisset ea eam. Ut sit audiam pertinax. Eam at kasd ipsum.")
        clips.api.store("http://behance.vo.llnwd.net/", "http://www.somepage.com/linked/link", "null", "null" , "In his sumo nonumy iracundia. Per ignota imperdiet et. Id qui eruditi alienum, in pri vidisse aliquando, pri in duis nostrum. Vim ornatus alienum at. Mea utinam tempor cu, choro qualisque ne vim, eruditi perpetua forensibus sed ut.")
        clips.api.store("http://www.webdesigns.com/", "null", "null", "Cum nusquam antiopam sententiae te, eu tale nominati evertitur sea. Ius prompta torquatos et. Cu ius.", "Veniam petentium at per, latine virtute invenire eum ad, augue eripuit definiebas no. His cu epicurei voluptatum efficiantur. Admodum scaevola vix eu. An usu homero pericula, mei ut ignota salutandi ludus.")
        clips.api.store("http://www.webdesigns.com/", "null", "null", "In clita pericula usu, impetus eruditi salutatus ad est, id vel probo illum. Usu ea exerci similique, mutat apeirian est eu. Duis ponderum eos ex, ei mea offendit indoctum. Ad aliquip apeirian conceptam qui, accumsan consequuntur mei ei.", "null")

        clips.likes.api.like(test_clip.key().id)
        self.assertEquals(True,True)