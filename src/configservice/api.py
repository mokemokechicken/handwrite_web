# coding: utf8
'''
Created on 2012/12/12

@author: k_morishita
'''
from configservice.services import service_get_config, service_list_config
from prjlib.django.view import json_response
from django.http import HttpResponseNotFound

def api_get_config(request, typename):
    success, response = service_get_config(typename)
    if success:
        return json_response(response)
    else:
        return HttpResponseNotFound()

def api_list_config(request):
    response = service_list_config()
    return json_response(response)
