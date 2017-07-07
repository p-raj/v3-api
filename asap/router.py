from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

if not getattr(settings, 'DEBUG', False):
    # disable API listings for the production server
    # that's the only difference between these two
    DefaultRouter = SimpleRouter


class Router(DefaultRouter):
    pass
