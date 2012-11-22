# coding: utf8
'''
Created on 2012/11/22

@author: k_morishita
'''


from prjlib.django.view import json_response
from web.services import service_post_hwdata
from django.views.decorators.csrf import csrf_view_exempt


@csrf_view_exempt
def api_hwdata(request):
    if request.method != "POST":
        return json_response({"message": "HTTP Method Error"})
    success, response = service_post_hwdata(request)
    if success:
        return json_response(response)
    else:
        return json_response({"error": response})

