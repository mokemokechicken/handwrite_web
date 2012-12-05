# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

from __future__ import absolute_import

import json
from django.test import TestCase

# from mock import patch
from web.models import HWData
from ..simple_n_direction import ConvertSimpleNDirection

class ConvertSimpleNDirectionTest(TestCase):
    def setUp(self):
        self.conv = ConvertSimpleNDirection(8)
    
    def test_encode_strokes(self):
        strokes = []
        strokes.append([[5,5], [8,5], [8,7]])
        strokes.append([[5,7], [5,5]])
        vectors = self.conv.encode_strokes(self.make_hwdata(strokes))
        #
        N=16
        v = vectors[0:N]
        self.assertEquals(0.3, v[0])
        self.assertEquals(0.3, sum(v))
        #
        v = vectors[N*1:N*2]
        self.assertEquals(0.2, v[2])
        self.assertEquals(0.2, sum(v))
        #
        v = vectors[N*2:N*3]
        self.assertEquals(0.3, v[4+8])
        self.assertEquals(0.3, sum(v))
        #
        v = vectors[N*3:N*4]
        self.assertEquals(0.2, v[6])
        self.assertEquals(0.2, sum(v))
        print vectors

    def make_hwdata(self, strokes, w=10, h=10):
        return HWData(width=w, height=w, char="x", strokes=json.dumps(strokes))
        