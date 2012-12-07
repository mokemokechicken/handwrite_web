# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''


from prjlib.django.view import json_response
from web.services import service_post_hwdata, service_infer_version,\
    service_get_check_data, service_data_checked, service_char_weight
from django.views.decorators.csrf import csrf_view_exempt
from django.http import HttpResponseBadRequest


@csrf_view_exempt
def api_hwdata(request, chartype):
    if request.method not in ("POST", "GET"):
        return json_response({"message": "HTTP Method Error"})
    if request.method == "POST":
        will_save = True
        data = request.raw_post_data
    else:
        will_save = False
        data = request.GET["json"]
    success, response = service_post_hwdata(request, chartype, data, will_save)
    if success:
        return json_response(response)
    else:
        return json_response({"error": response})

def api_version(request, chartype):
    ret = service_infer_version(chartype)
    return json_response(ret)

def api_check_data(request, chartype):
    success, response = service_get_check_data(request, chartype)
    if success:
        return json_response(response)
    else:
        return HttpResponseBadRequest(response)

@csrf_view_exempt
def api_checked(request, chartype):
    success, response = service_data_checked(request, chartype)
    if success:
        return json_response(response)
    else:
        return HttpResponseBadRequest(response)


def api_char_weight(request, chartype):
    success, response = service_char_weight(request, chartype)
    if success:
        return json_response(response)
    else:
        return HttpResponseBadRequest(response)
    