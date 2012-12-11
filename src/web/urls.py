# coding: utf8

from __future__ import absolute_import

from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from .views import page_index, page_training, page_top, page_check_data, page_find_error
from .apis import api_hwdata, api_version, api_check_data, api_checked, api_char_weight, api_find_error


default_chartype = "num_hira"

urlpatterns = patterns('',
    url(r'^(?P<chartype>[^./]+)/training$', page_training),
    url(r'^(?P<chartype>[^./]+)/check_data$', page_check_data),
    url(r'^(?P<chartype>[^./]+)/find_error$', page_find_error),
    url(r'^(?P<chartype>[^./]+)/$', page_index),
    url(r'^$', page_top),
    
    # API
    url(r'(?P<chartype>[^./]+)/api/hwdata', api_hwdata),
    url(r'(?P<chartype>[^./]+)/api/check_data', api_check_data),
    url(r'(?P<chartype>[^./]+)/api/checked', api_checked),
    url(r'(?P<chartype>[^./]+)/api/version', api_version),
    url(r'(?P<chartype>[^./]+)/api/char_weight', api_char_weight),
    url(r'(?P<chartype>[^./]+)/api/find_error', api_find_error),
    url(r'api/hwdata', api_hwdata, {"chartype": default_chartype}),
)
