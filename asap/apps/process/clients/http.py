#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging

import requests
from coreapi import Client, exceptions
from coreapi.transports import HTTPTransport
from django.core.exceptions import ValidationError

from asap.utils import dot_to_json

logger = logging.getLogger(__name__)


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

            encoding = __params.get('__encoding', 'application/json')
            headers = {'Host': self.document.url, 'Content-type': encoding}
            logger.debug('encoding: %s', encoding)

            if encoding == 'text/plain':
                # FIXME
                resp = requests.request(
                    self.document['api'].action,
                    self.document['api'].url.format(**body),
                    data=body.get('body'),
                    headers=headers
                )
                return resp.json()

            # only for multipart/form-data
            if encoding == 'multipart/form-data':
                for k, v in body.items():
                    # hack for json items in multipart/form-data :(
                    body[k] = v if type(v) != dict else json.dumps(v)

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
