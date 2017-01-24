#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- utils.validator
~~~~~~~~~~~~~~~~~

- This file contains common validation functions.
"""

# future
from __future__ import unicode_literals

# 3rd party
import ujson as json


def _get_bad_strings_json():
    """
    ref : https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.json

    :return: bad string json object.
    """
    json_data = open('static/bad_strings.json').read()
    return json.loads(json_data)