# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from web.models import HWData
from web.model_converter import convert_strokes_to_16signals, convert_strokes_simply
from cStringIO import StringIO
import csv
from handwrite_web.data_config import get_chars

NUMINS = 16 * 50

def get_data_service(request, chartype):
    noise_range = request.GET.get("noise_range")
    multiply = int(request.GET.get("multiply", 1))
    char_map = get_char_map(get_chars(chartype))
    hwdataset = HWData.objects.filter(char__in = char_map.keys())
    numouts = len(char_map.keys())
    buf = StringIO()
    writer = csv.writer(buf)
    if noise_range:
        noise_range = [float(x) for x in noise_range.split(",")]
    for hwdata in hwdataset:
        sdata = convert_strokes_simply(hwdata)
        for _ in range(multiply):
            in_x = convert_strokes_to_16signals(sdata, noise_range=noise_range)
            if len(in_x) < NUMINS:
                in_x.extend([0] * (NUMINS-len(in_x)))
            #
            out = char_map[hwdata.char]
            #
            writer.writerow([str(x) for x in ([hwdata.id] + in_x + [out])])
    #
    info = {
            "in": NUMINS,
            "out": numouts,
            "row": len(hwdataset) * multiply,
            }
    data = buf.getvalue()
    buf.close()
    return data, info
    

def get_char_map(chars):
    retmap = {}
    for index, char in enumerate(chars):
        retmap[char] = index
    return retmap
