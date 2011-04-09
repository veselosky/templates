from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from {{ project_name }}.urls import urlpatterns

urlpatterns += staticfiles_urlpatterns
