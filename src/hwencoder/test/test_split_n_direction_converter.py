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
from ..split_n_direction import ConvertSplitNDirection
import math

class ConvertSplitNDirectionTest(TestCase):
   
    def test_encode_strokes_8(self):
        self.conv = ConvertSplitNDirection(8)
        strokes = []
        strokes.append([[5,5], [8,5], [8,7]])
        strokes.append([[5,7], [6,5]]) 
        vectors = self.conv.encode_strokes(self.make_hwdata(strokes))
        #
        N = self.conv.num_in
        v = vectors[0:N]
        self.assertEquals(0.3, v[0])
        self.assertEquals(0.3, sum(v))
        #
        v = vectors[N*1:N*2]
        self.assertAlmostEquals(0.2, v[2], delta=0.00001)
        self.assertEquals(0.2, sum(v))
        #
        v = vectors[N*2:N*3] # -0.3, 0
        self.assertAlmostEquals(0.3, v[4+self.conv.n_direction])
        self.assertAlmostEquals(0.3, sum(v))
        #
        v = vectors[N*3:N*4] # 0.1, -0.2
        dx6, dy6 = math.cos(math.radians(270)), math.sin(math.radians(270))
        dx7, dy7 = math.cos(math.radians(315)), math.sin(math.radians(315))
        self.assertTrue(v[6] > 0)
        self.assertTrue(v[7] > 0)
        self.assertAlmostEquals(0.1, dx6*v[6]+dx7*v[7])
        self.assertAlmostEquals(-0.2, dy6*v[6]+dy7*v[7])

    def test_encode_strokes_4(self):
        self.conv = ConvertSplitNDirection(4)
        strokes = []
        strokes.append([[5,5], [8,6], [8,7]])
        strokes.append([[5,7], [5,5]])
        vectors = self.conv.encode_strokes(self.make_hwdata(strokes))
        #
        N = self.conv.num_in
        v = vectors[0:N] # 0.3, 0.1
        self.assertAlmostEquals(0.3, v[0])
        self.assertAlmostEquals(0.1, v[1])
        self.assertEquals(0.4, sum(v))
        #
        v = vectors[N*1:N*2] # 0, 0.1
        self.assertEquals(0.1, v[1])
        self.assertEquals(0.1, sum(v))
        #
        v = vectors[N*2:N*3] # -0.3, 0
        self.assertEquals(0.3, v[2+self.conv.n_direction])
        self.assertAlmostEquals(0.3, sum(v), delta=0.00001)
        #
        v = vectors[N*3:N*4] # 0, -0.2
        self.assertEquals(0.2, v[3])
        self.assertAlmostEquals(0.2, sum(v), delta=0.00001)


    def make_hwdata(self, strokes, w=10, h=10):
        return HWData(width=w, height=w, char="x", strokes=json.dumps(strokes))
        