"""
Web hooks are a standard interface that transfers state changes over HTTP.

We need web hooks to make sure the events are
transmitted to our server that orchestrates things.

"""
from django.contrib import admin
from django.db import models

from apps.terminals.models.event import Event


class WebHook(models.Model):
    """
    Reference: https://developer.github.com/webhooks/
    """
    # http://stackoverflow.com/a/417184/1796173
    endpoint = models.URLField(max_length=2048)

    # we might end up deactivating a
    # web hook rather than deleting it
    is_active = models.BooleanField(default=True)

    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.endpoint

    def fire(self, payload):
        import requests
        # TODO
        # save the request id etc to enable analytics
        requests.post(self.endpoint, data=payload)


@admin.register(WebHook)
class WebHookAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'is_active']
