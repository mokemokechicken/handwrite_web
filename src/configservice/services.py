# coding: utf8
'''
Created on 2012/12/12

@author: k_morishita
'''
from configservice.models import TypeInfo

def service_get_config(typename):
    query = TypeInfo.objects.filter(typename=typename)[:1]
    if len(query) == 0:
        return False, None
    return True, {"config": query[0].to_dict()}


def service_list_config():
    query = TypeInfo.objects.all()
    ret = [m.to_dict() for m in query]
    return ret


