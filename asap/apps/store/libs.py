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
from bravado.exception import HTTPNotFound, HTTPBadRequest
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

    def callable_operation(self, operation, logging_cls, data={}):
        """

        :param operation: operation of swagger client
        :param data: payload to be sent with operation
        :param logging_cls: Logging class instance
        :return: depends on operation
        """
        api_token = None # in case of resource actor token is allowed null.
        logging_cls.handshake(api_token, data)  # execution handover initiated
        import ipdb;ipdb.set_trace()

        opt = CallableOperation(operation)
        try:
            opt.__call__(**data)
            result, response = operation(**data).result()
            logging_cls.handshake_succeed(api_token, data, response)  # execution handover status
            return response.json()
        except SwaggerMappingError as e:
            err = {'detail': ' {0}'.format(e)}
            logging_cls.handshake_failed(api_token, data, 400, err)  # execution handover status
            raise ValidationError()
        except (HTTPNotFound, HTTPBadRequest) as e:
            err = {'detail': ' {0}'.format(e)}
            logging_cls.handshake_failed(api_token, data, 400, err)  # execution handover status
            raise ValidationError({'detail': ' {0}'.format(e)})

