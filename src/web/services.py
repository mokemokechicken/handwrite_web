# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import json
from web.models import HWData
from web.model_converter import convert_strokes_simply,\
    convert_strokes_to_16signals

NUMINS = 16*50

def service_post_hwdata(request, data, will_save):
    try:
        hwdata = json.loads(data)
        meta = hwdata["meta"]
        model = HWData()
        model.width = meta["size"][0]
        model.height = meta["size"][1]
        model.char = hwdata["char"]
        model.strokes = json.dumps(hwdata["strokes"])
        if will_save:
            model.save()
        simple_hwdata = convert_strokes_simply(model)
        ######################################
        ######################################
        ######################################
        in_x = convert_strokes_to_16signals(simple_hwdata)
        if len(in_x) < NUMINS:
            in_x.extend([0] * (NUMINS-len(in_x)))
        ys = service_infer(in_x)
        ######################################
        ######################################
        ######################################
        
        return True, {"success": True, "strokes": json.loads(simple_hwdata.strokes),
                      "ys": ys
                      }
    except Exception, e:
        return False, repr(e)

from interface import Infer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
def service_infer(xs):
    
    # Make socket
    transport = TSocket.TSocket('localhost', 9999)
    
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    # Create a client to use the protocol encoder
    client = Infer.Client(protocol)
    
    # Connect!
    transport.open()
    
    return client.infer(xs)
