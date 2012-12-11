# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import json

from hwencoder.common import convert_strokes_simply, calc_direction,\
    calc_distance

class ConvertSimpleNDirection(object):
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
                direction = calc_direction(last_point, prev_point, n_direction, noise_range=noise_range)
                distance = calc_distance(last_point, prev_point, hwdata.width, hwdata.height, noise_range=noise_range)
                vector = [0] * self.num_in
                vector[direction+n_direction] = distance
                output.extend(vector)
            for point in stroke[1:]:
                direction = calc_direction(prev_point, point, n_direction, noise_range=noise_range)
                distance = calc_distance(prev_point, point, hwdata.width, hwdata.height, noise_range=noise_range)
                vector = [0] * self.num_in
                vector[direction] = distance
                output.extend(vector)
                prev_point = point
            last_point = prev_point
        return output
    
    def convert_strokes_simply(self, hwdata):
        """
        
        @param hwdata: HWData
        @return Simplified HWData Model 
        """
        return convert_strokes_simply(hwdata, 8, 0.02)

