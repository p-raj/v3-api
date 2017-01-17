#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
-store.libs
~~~~~~~~~~~~~~

-   This file contains the third party library classes/functions which we are going to use in store module.
    so every request to third party will goes from here so in future if we replace any lib with another our
    core code will not be changed , wer just needs to update this file.

-   Here we will create a proxy class for actual lib which will reverse proxy the request to that lib.

 """

# future
from __future__ import unicode_literals

# 3rd party libs
from bravado.client import SwaggerClient,  CallableOperation
from bravado_core.exception import SwaggerMappingError

# rest-framework
from rest_framework.exceptions import ValidationError


class BravadoLib(object):
    """A Proxy class of Bravado library

    ref : https://github.com/Yelp/bravado
    """

    def get_client_from_spec(self, spec_dict, origin_url):
        """It fetches teh swagger clint object from dict()

        :param origin_url: the url used to retrieve the resource schema
        :param spec_dict: holds the swagger dict
        :return: swagger client object
        """
        return SwaggerClient.from_spec(spec_dict, origin_url, config={'also_return_response': True})

    def callable_operation(self, operation, data={}):
        """

        :param operation: operation of swagger client
        :param data: payload to be sent with operation
        :return: depends on operation
        """

        opt = CallableOperation(operation)
        opt.__call__(**data)
        try:
            result, response = operation(**data).result()
            return response.json()
        except (SwaggerMappingError) as e:
            raise ValidationError({'detail': ' {0}'.format(e)})
