# coding: utf8
# Create your views here.
from prjlib.django.view import http_response

from handwrite_web.data_config import get_chars

def page_index(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/index.tmpl", tdict)

def page_training(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/training.tmpl", tdict)

def page_top(request):
    return http_response(request, "web/top.tmpl", {})

def page_check_data(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/check_data.tmpl", tdict)

