from django.conf.urls.defaults import *
from django.conf import settings

from {{ project_name }}.urls import urlpatterns

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)