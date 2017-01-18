#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
-store.resource
~~~~~~~~~~~~~~

-   This file contains classes/functions related to Resources

 """

# future
from __future__ import unicode_literals


# own app
from asap.apps.store import libs

class Resource(object):
    """A Resource object for accessing various resource operations and RESTful service.

    """
    logging_cls = None

    def __init__(self, logging_cls):
        """

        :param logging_cls: Logging class instance.
        """
        self.logging_cls = logging_cls

    def get_bravado_cls(self):
        """

        :return: Bravado class instance.
        """
        return libs.BravadoLib()

    def get_swagger_client(self, url, resource_schema,):
        """

        :param url: the url used to retrieve the resource schema
        :param resource_schema: resource swagger schema
        :return: resource swagger client object
        """
        return self.get_bravado_cls().get_client_from_spec(resource_schema, url)

    def execute_operation(self, url, resource_schema, operation_id, data={}):
        """

        :param url: the url used to retrieve the resource schema
        :param resource_schema: resource swagger schema
        :param operation_id: resource operation
        :param data : payload to be sent with operation
        :return: depends on operation response
        """
        _request_options = {'headers': {'Authorization': 'Bearer F4ZCjqiUHVNoSBH8mhwnKzuP25Vqzc'}}
        data.update({'_request_options': _request_options})

        client = self.get_swagger_client(url, resource_schema)
        operation = getattr(client.v1, operation_id)

        return self.get_bravado_cls().callable_operation(operation, self.logging_cls, data)
