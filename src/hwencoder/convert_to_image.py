# coding: utf8
'''
Created on 2012/12/13

@author: k_morishita
'''
import json

from PIL import Image, ImageDraw
from PIL.Image import BILINEAR


class ConvertToImage(object):
    def __init__(self, size=None):
        self.size = size or 30
        self.num_in = self.size * self.size

    def encode_strokes(self, hwdata, noise_range=None):
        image = Image.new("L", (hwdata.width, hwdata.height), 0)
        draw = ImageDraw.Draw(image)
        for stroke in json.loads(hwdata.strokes):
            points = [(p[0],p[1]) for p in stroke]
            draw.line(points, width=2, fill=255)
        image = image.resize((self.size, self.size), BILINEAR)
        return [x/255.0 for x in image.getdata()]
    
    def convert_strokes_simply(self, hwdata):
        """
        
        @param hwdata: HWData
        @return Simplified HWData Model 
        """
        return hwdata
