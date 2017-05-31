#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging
from functools import reduce

from coreapi import exceptions, Client
from coreapi.transports import HTTPTransport
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


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
        self.client = Client(
            transports=[self.transport],
            **kwargs
        )

    def execute(self, *args, **kwargs):
        logger.debug('kwargs: %s', kwargs)
        try:
            # TODO
            # documentation :/
            __params = {}
            body = dot_to_json(kwargs.get('params', {}))
            for key in list(body.keys()):
                if key.startswith('__'):
                    __params[key] = body.pop(key, None)

            encoding = __params.get('__encoding', 'multipart/form-data')
            logger.debug('encoding: %s', encoding)

            # only for multipart/form-data
            if encoding == 'multipart/form-data':
                for k, v in body.items():
                    # hack for json items in multipart/form-data :(
                    body[k] = v if type(v) != dict else json.dumps(v)

            headers = {'Host': self.document.url, 'Content-type': encoding}
            for field in self.document['api'].fields:
                if field.location == 'header' and body.get(field.name, None):
                    headers[field.name] = body[field.name]

            self.transport = HTTPTransport(headers=headers)
            self.client = Client(transports=[self.transport])

            data = self.client.action(
                self.document, ['api'], body,
                # FIXME
                # this should be based on whether
                # we are getting files or not
                encoding=encoding
            )
        except exceptions.ErrorMessage as e:
            logger.warning('exception: %s', e, exc_info=1)
            return e.error
        except exceptions.ParseError as e:
            logger.warning('exception: %s', e, exc_info=1)
            return e.args
        except exceptions.ParameterError as e:
            logger.warning('exception: %s', e, exc_info=1)
            raise ValidationError(e)
        return data
