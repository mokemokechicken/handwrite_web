# coding: utf8

from __future__ import absolute_import

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from .views import page_index, page_training
from .apis import api_hwdata


urlpatterns = patterns('',
    url(r'^training$', page_training),
    url(r'^$', page_index),
    
    # API
    url(r'api/hwdata', api_hwdata),
)
