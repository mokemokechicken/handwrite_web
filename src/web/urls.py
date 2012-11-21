from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from views import page_index

urlpatterns = patterns('',
    url(r'^$', page_index),
)
