# coding: utf8
'''
Created on 2012/01/31

@author: k_morishita
'''
from functools import wraps
from django.http import HttpResponseForbidden

YUMEMI_IP_SET = set([
                     "113.43.73.18",
                     "127.0.0.1",
                     ])

def is_remote_addr_in_yumemi(request):
    remote_ip = request.META.get("REMOTE_ADDR")
    return remote_ip in YUMEMI_IP_SET

def enable_only_from_yumemi(view):
    @wraps(view)
    def f(request, *args, **kw):
        if is_remote_addr_in_yumemi(request):
            return view(request, *args, **kw)
        else:
            return HttpResponseForbidden("社内からのみアクセス可能です")
    return f

