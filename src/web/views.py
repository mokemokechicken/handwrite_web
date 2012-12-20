# coding: utf8
# Create your views here.
from prjlib.django.view import http_response

from prjlib.django.middleware.httpauth import http_login_required
private_area = http_login_required(realm='HandWrite Demo')


from handwrite_web.data_config import get_chars

def page_index(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/index.tmpl", tdict)

@private_area
def page_training(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/training.tmpl", tdict)

def page_top(request):
    return http_response(request, "web/top.tmpl", {})

@private_area
def page_check_data(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/check_data.tmpl", tdict)

def page_find_error(request, chartype):
    tdict = {}
    tdict["chars"] = get_chars(chartype)
    return http_response(request, "web/find_error.tmpl", tdict)
