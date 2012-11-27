# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''
from dataservice.services import get_data_service
from django.http import HttpResponse

def api_hw_numbers_service(request):
    data, info = get_data_service(request)
    response = HttpResponse(data, mimetype="text/csv")
    response["X-LearnData-InNodeQty"] = info["in"]
    response["X-LearnData-OutNodeQty"] = info["out"]
    response["X-LearnData-RowQty"] = info["row"]
    return response
