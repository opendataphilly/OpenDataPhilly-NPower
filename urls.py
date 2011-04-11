from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    (r'^$', 'opendata.views.home'),
    (r'^opendata/$', 'opendata.views.results'),
    
    (r'^opendata/tag/(?P<tag_id>.*)/$', 'opendata.views.tag_results'),
    (r'^opendata/search/$', 'opendata.views.search_results'),
    (r'^opendata/resource/(?P<resource_id>.*)/$', 'opendata.views.resource_details'),
    
    (r'^tags/$', 'opendata.views.get_tag_list'),
    
    (r'^comments/', include('django.contrib.comments.urls')), 
    (r'^accounts/', include('registration.backends.default.urls')),


    # Uncomment the next line to enable the admin:
    url(r'^_admin_/', include(admin.site.urls)),
    #(r'^accounts/', include('registration.backends.default.urls')),

    (r'^/static/admin_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ADMIN_MEDIA_ROOT}), 
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DATA}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
