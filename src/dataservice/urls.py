from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from apis import api_data_service

urlpatterns = patterns('',
    # API
    url(r'api/dataset/(?P<chartype>[^/]+)$', api_data_service),
)
