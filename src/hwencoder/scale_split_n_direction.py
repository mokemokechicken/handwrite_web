# coding: utf8
'''
Created on 2012/12/11

@author: k_morishita
'''
from hwencoder.split_n_direction import ConvertSplitNDirection
from hwencoder.common import convert_strokes_simply
from web.models import HWData
import json


class ConvertScaleSplitNDirection(ConvertSplitNDirection):
    def convert_strokes_simply(self, hwdata):
        """hwdataの CanvasSize をいじる"""
        sdata = HWData.copy(hwdata)
        min_x = min_y = max(hwdata.width, hwdata.height)
        max_x = max_y = 0
        for stroke in json.loads(sdata.strokes):
            for point in stroke:
                min_x = min(min_x, point[0])
                max_x = max(max_x, point[0])
                min_y = min(min_y, point[1])
                max_y = max(max_y, point[1])
        rate = min(sdata.width*0.7/(max_x - min_x), sdata.height*0.7/(max_y-min_y))
        sdata.width /= rate
        sdata.height /= rate
        return convert_strokes_simply(sdata, 8, 0.03)
        