"""
An Action can just be considered an endpoint
optionally altering a resource on web.

An Action is provided by a `Service` and can't exist without it.
# It is recommended to read documentation on `Service` before proceeding.

Examples:
    - Create a log                  - POST /terminal-log
    - Add a member                  - POST /members
    - Fetch Invite Details          - GET /invite/:id

"""
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db import models

HTTP_METHODS = [
    ('GET', _('GET')),
    ('POST', _('POST')),
    ('PUT', _('PUT')),
    ('PATCH', _('PATCH')),
    ('DELETE', _('DELETE')),
    ('OPTIONS', _('OPTIONS')),
    ('HEAD', _('HEAD')),
    ('TRACE', _('TRACE'))
]


class Action(models.Model):
    # a friendly name to be given to it
    name = models.CharField(max_length=64)

    # http://stackoverflow.com/a/417184/1796173
    endpoint = models.URLField(max_length=2048)

    # GET,_()) PUT,_()) POST,_()) ....
    http_method = models.CharField(max_length=32, choices=HTTP_METHODS)

    # let's keep things simple for now,_())
    # this thing can get pretty complex
    # for instance
    # some endpoints may work asynchronously and give callbacks when done
    # data,_()) params,_()) caching,_()) filters,_()) content-type,_()) scheme
    # authorization headers,_()) etc....

    def __str__(self):
        return self.name


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    pass
