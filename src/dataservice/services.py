# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from web.models import HWData
from web.model_converter import convert_strokes_to_16signals, convert_strokes_simply
from cStringIO import StringIO
import csv

NUMINS = 16 * 50

def get_data_service(request):
    char_map = get_char_map()
    hwdataset = HWData.objects.filter(char__in = char_map.keys())
    numouts = len(char_map.keys())
    buf = StringIO()
    writer = csv.writer(buf)
    for hwdata in hwdataset:
        sdata = convert_strokes_simply(hwdata)
        in_x = convert_strokes_to_16signals(sdata)
        if len(in_x) < NUMINS:
            in_x.extend([0] * (NUMINS-len(in_x)))
        #
        out = char_map[hwdata.char]
        out_array = ["0"] * numouts
        out_array[out] = "1"
        #
        writer.writerow([str(x) for x in ([hwdata.id] + in_x + out_array)])
    #
    info = {
            "in": NUMINS,
            "out": numouts,
            "row": len(hwdataset),
            }
    data = buf.getvalue()
    buf.close()
    return data, info
    

def get_char_map(chars=u"０１２３４５６７８９"):
    retmap = {}
    for index, char in enumerate(chars):
        retmap[char] = index
    return retmap
