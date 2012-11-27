from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from apis import api_hw_numbers_service

urlpatterns = patterns('',
    # API
    url(r'api/hw_numbers', api_hw_numbers_service),
)
