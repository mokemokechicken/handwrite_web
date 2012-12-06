from django.conf.urls import patterns, include, url
from handwrite_web.settings import STATICFILES_DIRS

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'handwrite_web.views.home', name='home'),
    # url(r'^handwrite_web/', include('handwrite_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include("dataservice.urls")),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : STATICFILES_DIRS[0]}),
    url(r'', include("web.urls")),
)
