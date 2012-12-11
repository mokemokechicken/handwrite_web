# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''

from __future__ import absolute_import

import math

from django.test import TestCase


from .. import common as c
from web.models import HWData
import json

class ConvertCommonTest(TestCase):

    def test_calc_distance(self):
        d = c.calc_distance([10,10], [13, 14], 10, 10)
        self.assertEquals(0.5, d)

        d = c.calc_distance([10,10], [13, 14], 10, 10, noise_range=[1.1,1.99])
        self.assertTrue(0.5 < d < 1.0)

    def test_calc_direction(self):
        d = c.calc_direction([10,10], [15,10], 8)
        self.assertEquals(0, d)
        d = c.calc_direction([10,10], [0,10], 8)
        self.assertEquals(4, d)
        d = c.calc_direction([0,0], [math.cos(math.radians(22)),math.sin(math.radians(22))], 8)
        self.assertEquals(0, d)
        d = c.calc_direction([0,0], [math.cos(math.radians(-22)),math.sin(math.radians(-22))], 8)
        self.assertEquals(0, d)
        d = c.calc_direction([0,0], [math.cos(math.radians(23)),math.sin(math.radians(23))], 8)
        self.assertEquals(1, d)
        d = c.calc_direction([0,0], [math.cos(math.radians(-23)),math.sin(math.radians(-23))], 8)
        self.assertEquals(7, d)
    
    def test_convert_strokes_simply_1(self):
        d1 = self.make_hwdata([[(50,50),(60,50),(70,50)]])
        sd1 = c.convert_strokes_simply(d1)
        self.assertEquals([[[50,50],[70,50]]], json.loads(sd1.strokes))
        
        d1 = self.make_hwdata([[(50,50),(51,50),(60,50),(69,49),(70,50),(80,50)]])
        sd1 = c.convert_strokes_simply(d1)
        self.assertEquals([[[50,50],[80,50]]], json.loads(sd1.strokes))
        
    def test_convert_strokes_simply_2(self):
        d1 = self.make_hwdata([[(50,50),(69,49),(70,50),(60,60),(80,60)]])
        sd1 = c.convert_strokes_simply(d1)
        self.assertEquals([[[50,50],[70,50],[60,60],[80,60]]], json.loads(sd1.strokes))
    
    def make_hwdata(self, strokes):
        return HWData(char="Z", width=100, height=100, strokes=json.dumps(strokes))

    def test_distance_point_and_line(self):
        self.assertAlmostEquals(1, c.distance_point_and_line([0,0], [1,0], [0,1],1,1))
        self.assertAlmostEquals(0.1, c.distance_point_and_line([1,1], [10,1], [0,2],10,10))
        self.assertAlmostEquals(39*math.sqrt(82)/82, c.distance_point_and_line([-1, 1], [8,2], [5,6],1,1))
        self.assertAlmostEquals(14/math.sqrt(5), c.distance_point_and_line([-1,-1], [2,-2.5], [3,4],1,1))
