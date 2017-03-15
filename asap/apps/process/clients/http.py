#!/usr/bin/python
# -*- coding: utf-8 -*-
import coreapi


class HttpClient(object):
    def __init__(self, document, **kwargs):
        self.document = document
        self.client = coreapi.Client(**kwargs)

    def execute(self, *args, **kwargs):
        try:
            data = self.client.action(self.document, ['api'], kwargs.get('params', {}))
        except coreapi.exceptions.ErrorMessage as e:
            return e.error
        except coreapi.exceptions.ParameterError as e:
            errors = {
                'errors': [_ for _ in e.args]
            }
            return coreapi.Error('Bad Request', errors)
        return data
