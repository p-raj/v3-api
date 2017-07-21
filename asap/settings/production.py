"""Production settings and globals."""

from os import environ
from os import getenv

from .base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(key):
    """
    Get the environment setting or return exception,
    if default is not set

    :param key:
    """
    try:
        return environ[key]
    except KeyError:
        error_msg = 'Set the {0} env variable'.format(key)
        raise ImproperlyConfigured(error_msg)


# ######### HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = [
    'apis.noapp.mobi'
]
# ######### END HOST CONFIGURATION


# ######### EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', getenv('EMAIL_HOST_PASSWORD', ''))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', getenv('EMAIL_HOST_USER', ''))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[{0}] '.format(SITE_NAME)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = environ.get('SERVER_EMAIL', 'noreply@{}.com'.format(SITE_NAME))

DEFAULT_FROM_EMAIL = SERVER_EMAIL
# ######### END EMAIL CONFIGURATION


# ######### DATABASE CONFIGURATION
DATABASES = {
    'default': {
        # https://docs.djangoproject.com/en/1.10/releases/1.9/#database-backends
        # The PostgreSQL backend (django.db.backends.postgresql_psycopg2)
        # is also available as django.db.backends.postgresql. :)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_setting('DATABASE_NAME'),
        'USER': get_env_setting('DATABASE_USER'),
        'PASSWORD': get_env_setting('DATABASE_PASSWORD'),
        'HOST': get_env_setting('DATABASE_HOST'),
        'PORT': getenv('DATABASE_PORT', 5432)
    }
}
# ######### END DATABASE CONFIGURATION


# ######### SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
# ######### END SECRET CONFIGURATION


# ######### SESSION CONFIGURATION
# See: https://docs.djangoproject.com/en/1.8/ref/settings/#session-expire-at-browser-close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# ######### END SESSION CONFIGURATION


# ######### APP CONFIGURATION
PRODUCTION_APPS = (
    # 'gunicorn',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS += PRODUCTION_APPS
# ######### END APP CONFIGURATION


# ######### CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
DEFAULT_CACHE_BACKEND = environ.get('DEFAULT_CACHE_BACKEND', 'django.core.cache.backends.memcached.MemcachedCache')
DEFAULT_CACHE_LOCATION = environ.get('DEFAULT_CACHE_LOCATION', '127.0.0.1:11211')

CACHES = {
    'default': {
        'BACKEND': DEFAULT_CACHE_BACKEND,
        'LOCATION': DEFAULT_CACHE_LOCATION
    }
}
# ######### END CACHE CONFIGURATION


# ######### DJANGO REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'bouncer.rest_framework.VerisAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'asap.utils.filters.django_filter.DjangoFilter',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}
# ######### END DJANGO REST FRAMEWORK CONFIGURATION


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
V3__API_GATEWAY = get_env_setting('V3__API_GATEWAY')

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
V3__HOST_SELF = getenv('V3__HOST_SELF', 'apis.veris.in')
V3__HOST_MISTRAL = getenv('V3__HOST_MISTRAL', 'mistral.veris.in')
V3__HOST_AUTHORIZATION = getenv('V3__HOST_AUTHORIZATION', 'am.veris.in')

# ######### PROJECT SPECIFIC CONFIGURATION
