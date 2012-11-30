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
    if request.method not in ("POST", "GET"):
        return json_response({"message": "HTTP Method Error"})
    if request.method == "POST":
        will_save = True
        data = request.raw_post_data
    else:
        will_save = False
        data = request.GET["json"]
    success, response = service_post_hwdata(request, data, will_save)
    if success:
        return json_response(response)
    else:
        return json_response({"error": response})

