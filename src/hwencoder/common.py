# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''
from web.models import HWData
import json
import random
import math

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


def calc_distance(prev_point, point, width, height, noise_range=None):
    dx, dy = calc_point_diff(prev_point, point, width, height, noise_range=noise_range)
    return math.sqrt(dx*dx+dy*dy)

def calc_point_diff(prev_point, point, width, height, noise_range=None):
    noise_x = noise_y = 1
    if noise_range:
        noise_x = random.uniform(*noise_range)
        noise_y = random.uniform(*noise_range)
    dx = ((float(point[0]) - float(prev_point[0])) / width) * noise_x
    dy = ((float(point[1]) - float(prev_point[1])) / height) * noise_y
    return dx, dy

