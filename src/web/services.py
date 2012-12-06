# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''

import json
from web.models import HWData
from handwrite_web.data_config import get_host_port, get_chars
from hwencoder.factory import create_converter
import logging
from dataservice.services import get_char_map, get_hwdataset


def service_post_hwdata(request, chartype, data, will_save):
    try:
        hwdata = json.loads(data)
        conv = create_converter(chartype)
        in_len = conv.num_in * conv.seq_len 
        meta = hwdata["meta"]
        model = HWData()
        model.width = meta["size"][0]
        model.height = meta["size"][1]
        model.char = hwdata["char"]
        model.strokes = json.dumps(hwdata["strokes"])
        if will_save:
            model.save()
        simple_hwdata = conv.convert_strokes_simply(model)
        ######################################
        ######################################
        ######################################
        in_x = conv.encode_strokes(simple_hwdata)
        if len(in_x) < in_len:
            in_x.extend([0] * (in_len-len(in_x)))
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
        logging.error(repr(e))
        return False, repr(e)

###########
from interface import Infer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
def make_infer_client(chartype):
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
    return client
    
def service_infer(chartype, xs):
    client = make_infer_client(chartype)
    return client.infer(xs)

def service_infer_version(chartype):
    client = make_infer_client(chartype)
    return json.loads(client.version())

###################################

def service_get_check_data(request, chartype):
    char_map = get_char_map(get_chars(chartype))
    q = get_hwdataset(char_map)
    d_models = q.filter(validated=False).order_by("fb_ok", "-fb_ng")[:1]
    ret = {}
    if len(d_models) == 1:
        d_model = d_models[0]
        ret["id"] = d_model.id
        ret["char"] = d_model.char
        ret["width"] = d_model.width
        ret["height"] = d_model.height
        ret["strokes"] = json.loads(d_model.strokes)
    else:
        ret["status"] = "No Data"
    return True, ret

def service_data_checked(request, chartype):
    THRESHOULD = 3
    if "id" not in request.POST or "result" not in request.POST:
        return False, "Invalid Request"
        
    m_id = request.POST["id"]
    result = request.POST["result"] == "ok"
    d_model = HWData.objects.get(id=m_id)
    if result:
        d_model.fb_ok += 1
        if d_model.fb_ok >= THRESHOULD:
            d_model.validated = True
            d_model.is_use = True
    else:
        d_model.fb_ng += 1
        if d_model.fb_ng >= THRESHOULD:
            d_model.validated = True
            d_model.is_use = False
    d_model.save()
    return True, {"fb_ok": d_model.fb_ok, "fb_ng": d_model.fb_ng}

