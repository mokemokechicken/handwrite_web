# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from cStringIO import StringIO
import csv

from web.models import HWData
from handwrite_web.data_config import get_chars
from hwencoder.factory import create_converter

def get_hwdataset(char_map):
    return HWData.objects.filter(char__in = char_map.keys())

def dataset_service(request, chartype):
    noise_range = request.GET.get("noise_range")
    multiply = int(request.GET.get("multiply", 1))
    char_map = get_char_map(get_chars(chartype))
    hwdataset = get_hwdataset(char_map)
    numouts = len(char_map.keys())
    conv = create_converter(chartype)
    in_len = conv.num_in * conv.seq_len
    #
    buf = StringIO()
    writer = csv.writer(buf)
    if noise_range:
        noise_range = [float(x) for x in noise_range.split(",")]
    for hwdata in hwdataset:
        sdata = conv.convert_strokes_simply(hwdata)
        for _ in range(multiply):
            in_x = conv.encode_strokes(sdata, noise_range=noise_range)
            if len(in_x) < in_len:
                in_x.extend([0] * (in_len-len(in_x)))
            #
            out = char_map[hwdata.char]
            #
            writer.writerow([str(x) for x in ([hwdata.id] + in_x + [out])])
    #
    info = {
            "in": in_len,
            "out": numouts,
            "row": len(hwdataset) * multiply,
            }
    data = buf.getvalue()
    buf.close()
    return data, info

def datainfo_service(request, chartype):
    multiply = int(request.GET.get("multiply", 1))
    char_map = get_char_map(get_chars(chartype))
    hwdata_count = HWData.objects.filter(char__in = char_map.keys()).count()
    numouts = len(char_map.keys())
    conv = create_converter(chartype)
    in_len = conv.num_in * conv.seq_len
    return True, {
        "in": in_len,
        "out": numouts,
        "row": hwdata_count * multiply,
    }

def get_char_map(chars):
    retmap = {}
    for index, char in enumerate(chars):
        retmap[char] = index
    return retmap
