from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from registration.views import register


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
    (r'^ideas/$', 'opendata.views.idea_results'),
    (r'^idea/(?P<idea_id>.*)/$', 'opendata.views.idea_results'),
    (r'^opendata/submit/$', 'opendata.views.suggest_content'),
    (r'^thanks/$', 'opendata.views.thanks'),    
    
    (r'^tags/$', 'opendata.views.get_tag_list'),
    
    (r'^comments/', include('django.contrib.comments.urls')), 
    url(r'^accounts/register/$',register,
           { 'backend': 'registration_backend.ODPBackend' },
       name='registration_register'),
    (r'^accounts/password_reset', 'django.contrib.auth.views.password_reset'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^opendata/nominate/', include('suggestions.urls')),
    

    # Uncomment the next line to enable the admin:
    url(r'^_admin_/', include(admin.site.urls)),

    (r'^/static/admin_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ADMIN_MEDIA_ROOT}), 
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DATA}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
