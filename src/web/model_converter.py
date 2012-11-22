# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

from web.models import HWData
import json
import math

def convert_strokes_to_16signals(hwdata):
    pass

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

def calc_distance(prev_point, point, width, height):
    dx = (float(point[0]) - float(prev_point[0])) / width
    dy = (float(point[1]) - float(prev_point[1])) / height
    return math.sqrt(dx*dx+dy*dy)
    

def calc_direction(prev_point, point, n_direction):
    dx = float(point[0]) - float(prev_point[0])
    dy = float(point[1]) - float(prev_point[1])
    unit_arg = ((2*math.pi)/n_direction)
    direction = round(math.atan2(dy, dx)/unit_arg) % n_direction
    return direction
    

