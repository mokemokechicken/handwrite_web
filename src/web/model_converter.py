# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

from web.models import HWData
import json
import math
import random

def convert_strokes_to_16signals(hwdata, n_direction=8, noise_range=None):
    output = []
    last_point = None
    for stroke in json.loads(hwdata.strokes):
        prev_point = stroke[0]
        if last_point:
            direction = calc_direction(last_point, prev_point, n_direction)
            distance = calc_distance(last_point, prev_point, hwdata.width, hwdata.height)
            vector = [0] * (n_direction*2)
            vector[direction+n_direction] = distance
            output.append(vector)
        for point in stroke[1:]:
            direction = calc_direction(prev_point, point, n_direction)
            distance = calc_distance(prev_point, point, hwdata.width, hwdata.height)
            vector = [0]* (n_direction*2)
            vector[direction] = distance
            output.append(vector)
            prev_point = point
        last_point = prev_point
    return output

def convert_strokes_simply(hwdata, n_direction=8, dist_threshold=0.05):
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
            elif calc_distance(ns[-1], point, sdata.width, sdata.height) >= dist_threshold:
                prev_direction = calc_direction(ns[-1], point, n_direction)
                direction = calc_direction(prev_point, point, n_direction)
                if direction != prev_direction:
                    ns.append(prev_point)
            prev_point = point
        if calc_distance(ns[-1], prev_point, sdata.width, sdata.height) >= dist_threshold:
            ns.append(prev_point)
    sdata.strokes = json.dumps(new_strokes)
    return sdata

def calc_distance(prev_point, point, width, height, noise_range=None):
    noise_x = noise_y = 1
    if noise_range:
        noise_x = random.uniform(*noise_range)
        noise_y = random.uniform(*noise_range)
    dx = ((float(point[0]) - float(prev_point[0])) / width) * noise_x
    dy = ((float(point[1]) - float(prev_point[1])) / height) * noise_y
    return math.sqrt(dx*dx+dy*dy)
    

def calc_direction(prev_point, point, n_direction, noise_range=None):
    noise_x = noise_y = 1
    if noise_range:
        noise_x = random.uniform(*noise_range)
        noise_y = random.uniform(*noise_range)
    dx = (float(point[0]) - float(prev_point[0])) * noise_x
    dy = (float(point[1]) - float(prev_point[1])) * noise_y
    unit_arg = ((2*math.pi)/n_direction)
    direction = round(math.atan2(dy, dx)/unit_arg) % n_direction
    return int(direction)
    

