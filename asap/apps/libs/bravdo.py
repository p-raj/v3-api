#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.libs.bravado
~~~~~~~~~~~~~~

-   This file contains the Bravdo third party library classes/functions which we are going to use in store module.
    so every request to third party will goes from here so in future if we replace any lib with another our
    core code will not be changed , wer just needs to update this file.

-   Here we will create a proxy class for actual lib which will reverse proxy the request to that lib.

 """

# future
from __future__ import unicode_literals

# 3rd party libs
from bravado.client import SwaggerClient


class BravadoLib(object):
    """A Proxy class of Bravado library

    ref : https://github.com/Yelp/bravado
    """

    def get_client_from_spec(self, origin_url, spec_dict):
        """It fetches teh swagger clint object from dict()

        :param origin_url: the url used to retrieve the resource schema
        :param spec_dict: holds the swagger dict
        :return: swagger client object
        """
        spec = SwaggerClient.from_spec(spec_dict, origin_url, config={'also_return_response': True})
        return spec

    def get_all_operations(self, swagger_spec):
        """
        :param swagger_spec: swagger client spec object
        :return: All operations
        """

        # loop over list of resources from spec, and retrieve operations for each resource
        ops = []
        for resource in dir(swagger_spec):
            d = {}
            resource_obj = swagger_spec.__getattr__(resource)
            d[resource] = resource_obj.__dir__()
            ops.append(d)
        return ops

