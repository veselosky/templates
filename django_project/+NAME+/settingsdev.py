from {{ project_name }}.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = '{{ project_name }}.urlsdev'
INSTALLED_APPS += ('debug_toolbar',)
CACHE_BACKEND = 'locmem://'
TEMPLATE_STRING_IF_INVALID = 'INVALID TEMPLATE VARIABLE'