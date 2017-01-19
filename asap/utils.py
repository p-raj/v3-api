#!/usr/bin/python
# -*- coding: utf-8 -*-

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
