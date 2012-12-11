# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''
from hwencoder.common import convert_strokes_simply, calc_point_diff
import json
import math
import numpy

class ConvertSplitNDirection(object):
    def __init__(self, n_direction, seq_len=None):
        self.n_direction = n_direction
        self.num_in = n_direction * 2
        self.seq_len = seq_len or 50

    def encode_strokes(self, hwdata, noise_range=None):
        n_direction = self.n_direction
        output = []
        last_point = None
        for stroke in json.loads(hwdata.strokes):
            prev_point = stroke[0]
            if last_point:
                vector = self.calc_vector(last_point, prev_point, n_direction, hwdata.width, hwdata.height, noise_range=noise_range)
                vv = ([0] * n_direction) + vector
                output.extend(vv)
            for point in stroke[1:]:
                vector = self.calc_vector(prev_point, point, n_direction, hwdata.width, hwdata.height, noise_range=noise_range)
                vector = vector + ([0] * n_direction)
                output.extend(vector)
                prev_point = point
            last_point = prev_point
        return output
        

    def calc_2direction(self, n_direction, dx, dy):
        unit_arg = (2 * math.pi) / n_direction
        direction = math.atan2(dy, dx) / unit_arg
        if direction < 0:
            direction += n_direction
        d1 = int(math.floor(direction))
        d2 = (d1 + 1) % n_direction
        return d1, d2

    def get_primary_vector(self, direction, n_direction):
        rad = 2 * math.pi / n_direction * direction
        return math.cos(rad), math.sin(rad)

    def calc_vector(self, prev_point, next_point, n_direction, width, height, noise_range=None):
        dx, dy = calc_point_diff(prev_point, next_point, width, height, noise_range=noise_range)
        d1, d2 = self.calc_2direction(n_direction, dx, dy)
        v1, v2 = self.get_primary_vector(d1, n_direction), self.get_primary_vector(d2, n_direction)
        mat = numpy.matrix([v1,v2])
        xs = numpy.array([dx,dy])
        ans = numpy.dot(mat.T.I, xs)
        vector = [0] * self.n_direction
        vector[d1] = ans[0,0]
        vector[d2] = ans[0,1]
        return vector
    
    def convert_strokes_simply(self, hwdata):
        """
        
        @param hwdata: HWData
        @return Simplified HWData Model 
        """
        return convert_strokes_simply(hwdata, 8, 0.03)
