# coding :utf8
'''
Created on 2012/12/13

@author: k_morishita
'''

from __future__ import absolute_import

import json
from django.test import TestCase

# from mock import patch

from web.models import HWData
from ..convert_to_image import ConvertToImage

class ConvertToImageTest(TestCase):
    def setUp(self):
        pass
   
    def make_hwdata(self, strokes, w=10, h=10, id=None):
        return HWData(id=id, width=w, height=w, char="x", strokes=json.dumps(strokes))

    def test_encode_strokes(self):
        strokes = [[(30,30),(240,240),(240,30)], [(30,120),(120,30)]]
        hwdata = self.make_hwdata(strokes, id=1,w=300,h=300)
        cti = ConvertToImage(size=30)
        output = cti.encode_strokes(hwdata)
        self.assertEquals(900, len(output))
        self.assertTrue(0 <= min(output))
        self.assertTrue(max(output) <= 1)
       
       

