# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import json
from web.models import HWData
from web.model_converter import convert_strokes_simply,\
    convert_strokes_to_16signals
from handwrite_web.data_config import get_host_port

NUMINS = 16*50

def service_post_hwdata(request, chartype, data, will_save):
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
        try:
            ys = service_infer(chartype, in_x)
        except:
            ys = [0] * 10
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
def service_infer(chartype, xs):
    host, port = get_host_port(chartype)
    # Make socket
    transport = TSocket.TSocket(host, port)
    
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    # Create a client to use the protocol encoder
    client = Infer.Client(protocol)
    
    # Connect!
    transport.open()
    
    return client.infer(xs)
