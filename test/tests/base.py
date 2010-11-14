'''
Created on Nov 7, 2010

@author: michalracek
'''

import unittest
import swaglr.api
import testutils

DEV_URL = "http://localhost:8081/api/clip/post/"

class TestLocalHost(unittest.TestCase):

        
        
    def test_valid_load(self):
        test_data = testutils.load_data("data/valid.csv")
        for data in test_data:
            print "Post data : %s" %  (data)
            res = swaglr.api.post(params=data,server_url=DEV_URL,verbose=True)
            self.assertEquals('OK',res['code'])

    def test_invalid_load(self):
        test_data = testutils.load_data("data/invalid.csv")
        for data in test_data:
            print "Post data : %s" %  (data)
            res = swaglr.api.post(params=data,server_url=DEV_URL,verbose=True)
            self.assertEquals('ERROR',res['code'])

