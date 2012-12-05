# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''

from __future__ import absolute_import

import math

from django.test import TestCase


from .. import common as c

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
