import logging

from django.db.models import Model

from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

logger = logging.getLogger(__name__)


class HyperlinkedSerializedRelatedField(serializers.HyperlinkedRelatedField):
    """
    Send in the serializer, and the object will be serialized by the serializer,
    not just the url :)

    It will also accept the json, and map it accordingly.
    Inspired by django-tastypie ``full=True`` feature.

    **auto creation of nested object is not supported here**

    """

    def __init__(self, view_name=None, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        assert self.serializer, ('the `serializer` argument is required. if not present use '
                                 '``rest_framework.serializers.HyperlinkedRelatedField``')

        super(HyperlinkedSerializedRelatedField, self).__init__(view_name=view_name, **kwargs)

    def use_pk_only_optimization(self):
        """
        ``HyperlinkedRelatedField`` sets it to true in case of default look up field

        lets not risk it and hard code it to ``False``

        We need the complete model instance in ``to_representation``
        and not just ``PKOnlyObject`` to serialize without querying again the database

        :return:
        """
        return False

    def get_representation(self, obj, serializer, context):
        """
        get the complete serialized representation of object,
        not just the url field

        :param obj:
        :param serializer:
        :param context:
        """
        if obj.pk is None:
            return None

        assert not isinstance(obj, PKOnlyObject), ('object only contains a PK, we don\'t '
                                                   'want to query the database again')

        assert obj is not None, (
            'Could not resolve URL for hyperlinked relationship using '
            'serializer "{}". You may have failed to include the related '
            'model in your API, or incorrectly configured the '
            '`lookup_field` attribute on this field.'
        ).format(self.serializer)

        _serializer = serializer(obj, context=context)
        return _serializer.data

    def to_representation(self, value):
        """
        Transform the *outgoing* native value into primitive data.

        :param value:
        :return:
        """

        if self.serializer:
            return self.get_representation(value, self.serializer, self.context)

        return super(HyperlinkedSerializedRelatedField, self).to_representation(value)

    def to_internal_value(self, data):
        """
        Transform the *incoming* primitive data into a native value.

        :param data: can be a dict or a string
        """
        if hasattr(data, '__class__') and issubclass(data.__class__, Model):
            # nested serializers often pass the instance of models
            # in that case directly return the incoming data
            return data

        if isinstance(data, str) and data.startswith('{'):
            # the data seems like a dict wrapped in string
            # lets evaluate it, and catch the exception if any
            try:
                data = eval(data)
            except SyntaxError as e:
                logger.exception(e.__dict__)

        if self.serializer and isinstance(data, dict):
            # the complete json is being sent back,
            # extract and pass the url as expected by the super class
            data = data.get('url', '')

        return super(HyperlinkedSerializedRelatedField, self).to_internal_value(data)
