from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

if not getattr(settings, 'DEBUG', False):
    # disable API listings for the production server
    # that's the only difference between these two
    DefaultRouter = SimpleRouter


class Router(DefaultRouter):
    """
    Credits: http://stackoverflow.com/a/22684199/1796173
    """
    shared_router = DefaultRouter()

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)
        super(Router, self).register(*args, **kwargs)
