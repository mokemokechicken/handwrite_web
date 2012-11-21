# Create your views here.
from django.http import HttpResponse
from prjlib.django.view import http_response


def page_index(request):
    tdict = {}
    return http_response(request, "web/index.tmpl", tdict)

