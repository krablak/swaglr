'''
Created on Nov 7, 2010

@author: michalracek
'''

import unittest
import swaglr.api
import testutils

DEV_URL = "http://localhost:8080/api/clip/post/"

class TestLocalHost(unittest.TestCase):

        
        
    def test_valid_load(self):
        test_data = testutils.load_data("data/valid.csv")
        for data in test_data:
            res = swaglr.api.post(params=data,verbose=True)
            self.assertEquals('OK',res['code'])

    def test_invalid_load(self):
        test_data = testutils.load_data("data/invalid.csv")
        for data in test_data:
            res = swaglr.api.post(params=data,verbose=True)
            self.assertEquals('ERROR',res['code'])

