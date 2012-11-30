# coding: utf8
# Create your views here.
from prjlib.django.view import http_response


def page_index(request):
    tdict = {}
    return http_response(request, "web/index.tmpl", tdict)

def page_training(request):
    tdict = {}
    return http_response(request, "web/training.tmpl", tdict)
