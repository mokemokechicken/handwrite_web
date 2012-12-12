# coding: utf8

from __future__ import absolute_import

from django.conf.urls import patterns, url
from .api import api_get_config, api_list_config


urlpatterns = patterns('',
    url(r'^(?P<typename>[^./]+)$', api_get_config),
    url(r'^$', api_list_config),
)
