from {{ project_name }}.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = '{{ project_name }}.urlsdev'

CACHE_BACKEND = 'dummy://'
TEMPLATE_STRING_IF_INVALID = 'INVALID TEMPLATE VARIABLE'

# Activate and configure django-debug-toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
