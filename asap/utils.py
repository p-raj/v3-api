#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import uuid


# noinspection PyProtectedMember
def media_folder(instance, filename):
    """
    convenience method that stores the uploaded files in directory named after the django app, model and object id
    viz.
    #. suppose an organization uploads the logo
      - it will be stored in /media/organizations/organization/<id>/<filename>.<extension>

    :param instance:    instance of model to which a file/image is being attached
    :param filename:    the name of file being uploaded by the user (needed to determine extension).
    :return:            path of the file where it should be stored
    """
    extension = filename.split('.')[-1] if len(filename.split('.')) > 1 else 'jpg'
    filename = "{}.{}".format(uuid.uuid1(), extension)

    # content_type = ContentType.objects.get_for_model(instance)
    # app_label = content_type.app_label
    # model_name = content_type.model

    # saves call to database every time a file is uploaded
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    return os.path.join(app_label, model_name, filename)


def to_pascal_case(text, split_chars='-_'):
    """
    # test default split_chars
    >>> to_pascal_case('to-pascal_case')
    'ToPascalCase'

    # test arg split_chars
    >>> to_pascal_case('to-pascal case', split_chars='- ')
    'ToPascalCase'

    :param text: a string to be converted to pascal case
    :param split_chars: string of characters which would mark the beginning of new word
    :return: PascalCase string
    """

    def gen_pascal_case():
        """
        capitalize each word as in PascalCase
        """
        while True:
            yield str.capitalize

    split_chars_regex = '[{}]'.format(split_chars)
    pascal_case = gen_pascal_case()
    return ''.join(next(pascal_case)(_) for _ in re.split(split_chars_regex, text))
