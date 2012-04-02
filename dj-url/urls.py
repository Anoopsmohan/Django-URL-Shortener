from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('', (r'^$', 'views.main'), (r'^posted$', 'views.posted'),
    (r'^(.+)$', 'views.forwardurl'),
    # Examples:
    # url(r'^$', 'graphcoloring.views.home', name='home'),
    # url(r'^graphcoloring/', include('graphcoloring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
