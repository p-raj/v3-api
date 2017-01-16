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
        :return: depends on operation response
        """
        client = self.get_swagger_client(url, resource_schema)
        operation = getattr(client.v1, operation_id)

        return self.get_bravado_cls().execute_operation(operation, data)
