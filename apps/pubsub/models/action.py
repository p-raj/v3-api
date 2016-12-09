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
from django.db import models

HTTP_METHODS = [
    'GET', 'POST',
    'PUT', 'PATCH',
    'DELETE',
    'OPTIONS', 'HEAD', 'TRACE'
]


class Action(models.Model):
    # a friendly name to be given to it
    name = models.CharField(max_length=64)

    # http://stackoverflow.com/a/417184/1796173
    endpoint = models.URLField(max_length=2048)

    # GET, PUT, POST, ....
    http_method = models.CharField(choices=HTTP_METHODS)

    # let's keep things simple for now,
    # this thing can get pretty complex
    # for instance
    # some endpoints may work asynchronously and give callbacks when done
    # data, params, caching, filters, content-type, scheme
    # authorization headers, etc....

    def __str__(self):
        return self.name
