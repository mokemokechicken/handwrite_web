# coding: utf8

from __future__ import absolute_import

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from .views import page_index, page_training, page_top
from .apis import api_hwdata, api_version



default_chartype = "numbers"

urlpatterns = patterns('',
    url(r'^(?P<chartype>[^./]+)/training$', page_training),
    url(r'^(?P<chartype>[^./]+)/$', page_index),
    url(r'^$', page_top),
    
    # API
    url(r'(?P<chartype>[^./]+)/api/hwdata', api_hwdata),
    url(r'(?P<chartype>[^./]+)/api/version', api_version),
    url(r'api/hwdata', api_hwdata, {"chartype": default_chartype}),
)
