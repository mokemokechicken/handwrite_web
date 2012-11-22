# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import json
from web.models import HWData
from web.model_converter import convert_strokes_simply


def service_post_hwdata(request, ):
    try:
        hwdata = json.loads(request.raw_post_data)
        meta = hwdata["meta"]
        model = HWData()
        model.width = meta["size"][0]
        model.height = meta["size"][1]
        model.char = hwdata["char"]
        model.strokes = json.dumps(hwdata["strokes"])
        model.save()
        simple_hwdata = convert_strokes_simply(model)
        return True, {"success": True, "strokes": json.loads(simple_hwdata.strokes)}
    except Exception, e:
        return False, repr(e)
