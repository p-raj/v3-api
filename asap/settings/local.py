"""Development settings and globals."""

from .base import *

# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# ######### END DEBUG CONFIGURATION

# ######### SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '*'
]
# ######### END SITE CONFIGURATION


# ######### EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = normpath(join(SITE_ROOT, 'emails'))
# ######### END EMAIL CONFIGURATION


# ######### DATABASE CONFIGURATION
DATABASES = {
    'default': {
        # https://docs.djangoproject.com/en/1.10/releases/1.9/#database-backends
        # The PostgreSQL backend (django.db.backends.postgresql_psycopg2)
        # is also available as django.db.backends.postgresql. :)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'v3',
        'HOST': '172.18.0.1',
        'USER': 'veris',
        'PASSWORD': 'veris',
        'PORT': '5432'
    }
}
# ######### END DATABASE CONFIGURATION


# ######### CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
# ######### END CACHE CONFIGURATION


# ######### TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions'
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TEMPLATE_CONTEXT': True
}
# ######### END TOOLBAR CONFIGURATION


# ######### PROJECT SPECIFIC CONFIGURATION
CELERY_ALWAYS_EAGER = True

# all the external calls must be through the gateway
# even the calls to our own services
# eg. mistral
# NOTE: at the beginning of the project the assumption
# was the process & widgets will separate micro-services
# which currently seems technically an overhead,
# and might be removed
# so for example the processes are fetched using
# HTTP request rather than direct access :(
V3__API_GATEWAY = 'http://172.20.0.1:8080'

# the api gateway looks for Host header
# to perform the proxy
# currently, we assume that everything will be proxied
# based on the Host header,
# we still don't know the shortcomings,
# so let's just wait for the problems & keep moving :)
# host self ? the header which will help the gateway
# identify on how to reach us (this server)!
# we are generating mistral workflow dynamically
# and we will need callbacks
V3__HOST_SELF = 'apis.veris.in'
V3__HOST_MISTRAL = 'mistral.veris.in'
V3__HOST_AUTHORIZATION = 'am.veris.in'

# ######### PROJECT SPECIFIC CONFIGURATION
