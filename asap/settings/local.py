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


# ######### JWT CONFIGURATION
# we need to create tokens for each service
# and adding table for each service seems like a lot of work
# so opting for simple JWT based library

# See: https://pyjwt.readthedocs.io/en/latest/algorithms.html#digital-signature-algorithms
AUDIENCE = 'noapp-services'
JWT_SECRET = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzj8vNzN+TPPeg4VJefx5dzvwJ' \
             'VvjLgRs+bd7iZbOl2JJnyNlMcMc5pJ2CrN+78IvnAsr/Vh57ZJEwy5y+MPxjjf8U5Lmlg' \
             'M65lpMN07I3SST8jRWYr1+KX50e7vvueYRY8y7sSkKVMIbqgu7tOfcsbsyk/MStuJQPFF' \
             'PBun0CuqA4JXvtQwS+y4Qb7UbjhmkCsfRzBiV34uODja8QjXWvdF/n01VGG4wd0898Pzb' \
             '7CogebMUvfGk7/3K82x1hZBotHxKDNYz/TPIr0+v/+MK5UxoLedHueMdwxJNtY2ska2wB' \
             'QQ0avN6EV5NMGV2k/OrP0kQ7cQwi6MW71IrwtntKwIDAQAB'
JWT_ALGORITHM = 'HS256'

# for backward support decoding
# don't remove a algorithm unless we want to
# completely throw away the tokens
JWT_ALGORITHMS = ['HS256']
# ######### END JWT CONFIGURATION


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
V3__API_GATEWAY = 'http://172.18.0.1:8080'

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
