# coding: utf8
'''
Created on 2012/12/13

@author: k_morishita
'''
import json

from PIL import Image, ImageDraw
from PIL.Image import BILINEAR, NEAREST, ANTIALIAS
import os


class ConvertToImage(object):
    def __init__(self, size=None):
        self.size = size or 30
        self.num_in = self.size * self.size
        self.seq_len = 1

    def __encode_strokes(self, hwdata, noise_range=None, image_save_path=None):
        image = Image.new("L", (hwdata.width, hwdata.height), 0)
        draw = ImageDraw.Draw(image)
        pw = int(hwdata.width * 0.02)
        for stroke in json.loads(hwdata.strokes):
            points = [(p[0],p[1]) for p in stroke]
            draw.line(points, width=pw, fill=255)
        image = image.resize((self.size, self.size), BILINEAR)
        ###
        if image_save_path:
            d = "%s/img%03d" % (image_save_path, int(hwdata.id / 100))
            if not os.path.exists(d):
                os.makedirs(d)
            image.save("%s/%05d.png" % (d, hwdata.id))
        return [x/255.0 for x in image.getdata()]

    def encode_strokes(self, hwdata, noise_range=None, image_save_path=None):
        image = Image.new("L", (self.size, self.size), 0)
        wr, hr = float(self.size)/hwdata.width, float(self.size)/hwdata.height 
        draw = ImageDraw.Draw(image)
        for stroke in json.loads(hwdata.strokes):
            points = [(p[0]*wr,p[1]*hr) for p in stroke]
            draw.line(points, width=1, fill=255)
        #image = image.resize((self.size, self.size), BILINEAR)
        ###
        if image_save_path:
            d = "%s/img%03d" % (image_save_path, int(hwdata.id / 100))
            if not os.path.exists(d):
                os.makedirs(d)
            image.save("%s/%05d.png" % (d, hwdata.id))
        return [x/255.0 for x in image.getdata()]

    
    def convert_strokes_simply(self, hwdata):
        """
        
        @param hwdata: HWData
        @return Simplified HWData Model 
        """
        return hwdata
