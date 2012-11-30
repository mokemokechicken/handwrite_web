# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''
from dataservice.services import dataset_service, datainfo_service
from django.http import HttpResponse
from prjlib.django.view import json_response

def api_dataset_service(request, chartype):
    data, info = dataset_service(request, chartype)
    response = HttpResponse(data, mimetype="text/csv")
    response["X-LearnData-InNodeQty"] = info["in"]
    response["X-LearnData-OutNodeQty"] = info["out"]
    response["X-LearnData-RowQty"] = info["row"]
    return response

def api_datainfo_service(request, chartype):
    success, info = datainfo_service(request, chartype)
    if success:
        return json_response(info)
    else:
        return HttpResponse(info, status=400)

