# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''
from web.models import HWData
import json
import random
import math

def convert_strokes_simply(hwdata, n_direction=8, dist_threshold=0.03):
    """
    
    @param hwdata: HWData
    @return Simplified HWData Model 
    """
    sdata = HWData.copy(hwdata)
    new_strokes = []
    for stroke in json.loads(sdata.strokes):
        ns = []
        mid_points = []
        new_strokes.append(ns)
        for point in stroke:
            if len(ns) == 0:
                ns.append(point)
            else:
                for mp in mid_points:
                    d = distance_point_and_line(ns[-1], point, mp, sdata.width, sdata.height)
                    if d > dist_threshold:
                        ns.append(mid_points[-1])
                        mid_points = []
                        break
            mid_points.append(point)
        if calc_distance(ns[-1], mid_points[-1], sdata.width, sdata.height) >= dist_threshold:
            ns.append(mid_points[-1])
    sdata.strokes = json.dumps(new_strokes)
    return sdata

def distance_point_and_line(p1, p2, p, W, H):
    """p1, p2 を結ぶ直線と点p との距離を求める。p1,p2は(x,y)なTuple"""
    a,b = (-1.0*(p2[1]-p1[1])/W, 1.0*(p2[0]-p1[0])/H)
    c = -(a*p1[0]/W+b*p1[1]/H)
    d = math.sqrt(a*a+b*b)
    if d == 0:
        return calc_distance(p1, p, W, H)
    return abs(a*p[0]/W+b*p[1]/H+c)/d

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

