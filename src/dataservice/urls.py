from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from apis import api_dataset_service, api_datainfo_service

urlpatterns = patterns('',
    # API
    url(r'api/dataset/(?P<chartype>[^/]+)$', api_dataset_service),
    url(r'api/datainfo/(?P<chartype>[^/]+)$', api_datainfo_service),
)
