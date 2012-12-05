# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import math
import json
from django.test import TestCase

# from mock import patch
from web.models import HWData
from ..simple_n_direction import ConvertSimpleNDirection

class ConvertSimpleNDirectionTest(TestCase):
    def setUp(self):
        self.conv = ConvertSimpleNDirection(8)
    
    def test_calc_distance(self):
        d = self.conv.calc_distance([10,10], [13, 14], 10, 10)
        self.assertEquals(0.5, d)

        d = self.conv.calc_distance([10,10], [13, 14], 10, 10, noise_range=[1.1,1.99])
        self.assertTrue(0.5 < d < 1.0)

    def test_calc_direction(self):
        d = self.conv.calc_direction([10,10], [15,10], 8)
        self.assertEquals(0, d)
        d = self.conv.calc_direction([10,10], [0,10], 8)
        self.assertEquals(4, d)
        d = self.conv.calc_direction([0,0], [math.cos(math.radians(22)),math.sin(math.radians(22))], 8)
        self.assertEquals(0, d)
        d = self.conv.calc_direction([0,0], [math.cos(math.radians(-22)),math.sin(math.radians(-22))], 8)
        self.assertEquals(0, d)
        d = self.conv.calc_direction([0,0], [math.cos(math.radians(23)),math.sin(math.radians(23))], 8)
        self.assertEquals(1, d)
        d = self.conv.calc_direction([0,0], [math.cos(math.radians(-23)),math.sin(math.radians(-23))], 8)
        self.assertEquals(7, d)

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
        