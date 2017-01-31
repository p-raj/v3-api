"""Development settings and globals."""

from .base import *

# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '*'
]
########## END SITE CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = normpath(join(SITE_ROOT, 'emails'))
########## END EMAIL CONFIGURATION



########## DATABASE CONFIGURATION
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
        'PORT': get_env_setting('DATABASE_PORT')
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
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
########## END TOOLBAR CONFIGURATION


########## PROJECT SPECIFIC CONFIGURATION
CELERY_ALWAYS_EAGER = True
########## PROJECT SPECIFIC CONFIGURATION


##### Micro Services UpStream Urls  ######
PROCESS_MICRO_SERVICE = get_env_setting('PROCESS_MICRO_SERVICE')
RESOURCE_MICRO_SERVICE = get_env_setting('RESOURCE_MICRO_SERVICE')
WIDGETS_MICRO_SERVICE = get_env_setting('WIDGETS_MICRO_SERVICE')
VRT_MICRO_SERVICE = get_env_setting('VRT_MICRO_SERVICE')


#
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         # Include the default Django email handler for errors
#         # This is what you'd get without configuring logging at all.
#         'mail_admins': {
#             'class': 'django.utils.log.AdminEmailHandler',
#             'level': 'ERROR',
#              # But the emails are plain text by default - HTML is nicer
#             'include_html': True,
#         },
#         # Log to a text file that can be rotated by logrotate
#         'logfile': {
#             'class': 'logging.handlers.WatchedFileHandler',
#             'filename': '/home/teramatrix/Documents/tmp.log'
#         },
#     },
#     'loggers': {
#         # Again, default Django configuration to email unhandled exceptions
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         # Might as well log any errors anywhere else in Django
#         'django': {
#             'handlers': ['logfile'],
#             'level': 'ERROR',
#             'propagate': False,
#         }
#     },
# }