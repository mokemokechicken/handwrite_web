# coding: utf8
# Create your views here.
from prjlib.django.view import http_response

from handwrite_web.data_config import get_chars

def page_index(request):
    tdict = {}
    tdict["chars"] = get_chars(get_charset_type(request))
    return http_response(request, "web/index.tmpl", tdict)

def page_training(request):
    tdict = {}
    tdict["chars"] = get_chars(get_charset_type(request))
    return http_response(request, "web/training.tmpl", tdict)

def get_charset_type(request):
    return request.GET.get("type", "numbers")
