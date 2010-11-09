'''
Created on Nov 7, 2010

@author: michalracek
'''

import unittest
import swaglr.api

DEV_URL = "http://localhost:8080/api/clip/post/"

class TestLocalHost(unittest.TestCase):


    def test_post(self):
        params = {'type' : 'LINK',
                  'page' : 'http://www.seznam.cz/',
                  'link' : 'http://www.seznam.cz/index.html',
                  'src' : 'null',
                  'text' : 'null',
                  'comment' : 'null' 
        }
        swaglr.api.post(params=params,verbose=True)
        self.assertTrue(True)
