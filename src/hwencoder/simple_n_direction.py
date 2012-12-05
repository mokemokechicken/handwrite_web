# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import json
import math
import random

from web.models import HWData

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
                direction = self.calc_direction(last_point, prev_point, n_direction, noise_range=noise_range)
                distance = self.calc_distance(last_point, prev_point, hwdata.width, hwdata.height, noise_range=noise_range)
                vector = [0] * self.num_in
                vector[direction+n_direction] = distance
                output.extend(vector)
            for point in stroke[1:]:
                direction = self.calc_direction(prev_point, point, n_direction, noise_range=noise_range)
                distance = self.calc_distance(prev_point, point, hwdata.width, hwdata.height, noise_range=noise_range)
                vector = [0] * self.num_in
                vector[direction] = distance
                output.extend(vector)
                prev_point = point
            last_point = prev_point
        return output
    
    def convert_strokes_simply(self, hwdata, n_direction=8, dist_threshold=0.05):
        """
        
        @param hwdata: HWData
        @return Simplified HWData Model 
        """
        sdata = HWData.copy(hwdata)
        new_strokes = []
        for stroke in json.loads(sdata.strokes):
            ns = []
            new_strokes.append(ns)
            prev_point = None
            for point in stroke:
                if len(ns) == 0:
                    ns.append(point)
                elif self.calc_distance(ns[-1], point, sdata.width, sdata.height) >= dist_threshold:
                    prev_direction = self.calc_direction(ns[-1], point, n_direction)
                    direction = self.calc_direction(prev_point, point, n_direction)
                    if direction != prev_direction:
                        ns.append(prev_point)
                prev_point = point
            if self.calc_distance(ns[-1], prev_point, sdata.width, sdata.height) >= dist_threshold:
                ns.append(prev_point)
        sdata.strokes = json.dumps(new_strokes)
        return sdata

    def calc_direction(self, prev_point, point, n_direction, noise_range=None):
        noise_x = noise_y = 1
        if noise_range:
            noise_x = random.uniform(*noise_range)
            noise_y = random.uniform(*noise_range)
        dx = (float(point[0]) - float(prev_point[0])) * noise_x
        dy = (float(point[1]) - float(prev_point[1])) * noise_y
        unit_arg = ((2*math.pi)/n_direction)
        direction = round(math.atan2(dy, dx)/unit_arg) % n_direction
        return int(direction)
    

    def calc_distance(self, prev_point, point, width, height, noise_range=None):
        noise_x = noise_y = 1
        if noise_range:
            noise_x = random.uniform(*noise_range)
            noise_y = random.uniform(*noise_range)
        dx = ((float(point[0]) - float(prev_point[0])) / width) * noise_x
        dy = ((float(point[1]) - float(prev_point[1])) / height) * noise_y
        return math.sqrt(dx*dx+dy*dy)
    

