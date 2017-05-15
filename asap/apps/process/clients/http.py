#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import reduce

import coreapi
from coreapi.transports import HTTPTransport
from django.core.exceptions import ValidationError


def dot_to_json(a):
    # TODO
    # move to utils
    output = {}
    for key, value in a.items():
        path = key.split('.')
        if path[0] == 'json':
            path = path[1:]
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = value
    return output


class HttpClient(object):
    def __init__(self, document, **kwargs):
        self.document = document
        self.transport = HTTPTransport(headers={'Host': self.document.url})
        self.client = coreapi.Client(
            transports=[self.transport],
            **kwargs
        )

    def execute(self, *args, **kwargs):
        try:
            # TODO
            # documentation :/
            body = dot_to_json(kwargs.get('params', {}))
            body = body if not body.get('data') else body.get('data')
            data = self.client.action(
                self.document, ['api'], body,
                # FIXME
                # this should be based on whether
                # we are getting files or not
                encoding='multipart/form-data'
            )
        except coreapi.exceptions.ErrorMessage as e:
            return e.error
        except coreapi.exceptions.ParameterError as e:
            raise ValidationError(e)
        return data
