# Django settings for {{ project_name }} project.
import os
import django

################
# Administrivia
MANAGERS = ADMINS = (('Vince Veselosky', 'vince@control-escape.com'),)
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# Make the SECRET_KEY unique, and don't share it with anybody.
SECRET_KEY = '{{ secret_key }}'
INTERNAL_IPS = ('127.0.0.1',)

################
# SITE SETTINGS
# If serving multiple sites, break these out to site-specific files.
SITE_ID = 1

##################
# DATABASE
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.', 
        'NAME': '',     # Or path to database file if using sqlite3.
        'USER': '',     # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '',     # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',     # Set to empty string for default. Not used with sqlite3.
    }
}

##################
# LOCALIZATION
# Vince note: I want Django to store all values as UTC. I'll translate
# them to local in templates if needed, hence the addition LOCAL*.
TIME_ZONE = 'UTC' # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
LOCAL_TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us' # http://www.i18nguy.com/unicode/language-identifiers.html
USE_I18N = True
USE_L10N = True

######################
# STATIC MEDIA
# Absolute path to the directory that holds uploaded media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/static/' % PROJECT_ROOT

# Absolute path to the directory that holds static media that ships with
# your project. From django-staticfiles.
STATIC_ROOT = '%s/static/' % PROJECT_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/", "/uploads/"
MEDIA_URL = '/site_media/'

# URL that handles the media served from STATIC_ROOT.
STATIC_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

######################
# CODE config

ROOT_URLCONF = '{{ project_name }}.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth', # see AUTHENTICATION
    # 'django.contrib.comments', # if you want native comments
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages', # see MESSAGES
    'django.contrib.redirects',
    'django.contrib.sessions', # see SESSIONS
    # 'django.contrib.sitemaps', # if you want them
    'django.contrib.sites',
    'south',
    'staticfiles',
)

TEMPLATE_DIRS = (
    # Example: "/home/html/django_templates" or "C:/www/django/templates".
    # Use absolute paths, not relative paths.
    '%s/templates' % PROJECT_ROOT
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware', # see CACHE
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # see SESSIONS
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # see CACHE
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth", # see AUTHENTICATION
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request", # not default
    "django.contrib.messages.context_processors.messages",
    'staticfiles.context_processors.static_url',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

######################
# SESSIONS
# Being a RESTafarian, I don't like sessions, but certain tools depend on them.
# The cache-only backend with locmem expires sessions on server restart,
# so we use write-through storage.
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_SAVE_EVERY_REQUEST = False # Change this and DIE!

######################
# CACHE
# Note: If you use cache-only storage for sessions, dummy doesn't work!
# Obviously we prefer memcached, so turn that on if you have it:
# CACHE_BACKEND = 'newcache://127.0.0.1:11211/?binary=true'
# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'locmem://'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_ROOT + SITE_ID
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# If using django-newcache, you may want these:
FLAVOR = 'prod'
CACHE_VERSION = 1

######################
# AUTHENTICATION
# AUTH_PROFILE_MODULE = None
# LOGIN_URL = '/accounts/login/'
# LOGOUT_URL = '/accounts/logout/'
# LOGIN_REDIRECT_URL = '/accounts/profile/'


######################
# MESSAGES
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'





