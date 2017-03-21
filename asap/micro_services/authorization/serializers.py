# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_services.authorization.serializers
~~~~~~~~~~~~~~

- This file contains the Authorization Serializers.
 """

# future
from __future__ import unicode_literals

# 3rd party
from datetime import datetime

# DRF
from rest_framework import serializers

# Django


# local

# own app
from asap.micro_services.authorization import models


class AuthorizationSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = models.Authorization
        exclude = ('id', 'token', 'created_at', 'modified_at',)

    def create(self, validated_data):
        """

        :param validated_data: Validated data sent by user
        :return: authorization object
        """
        validated_data.update({
            'created_at': datetime.now(),
            'modified_at': datetime.now(),
        })
        return models.Authorization.objects.create(**validated_data)


class CheckAccessSerializer(serializers.Serializer):
    """Serializer for checking Access of source over target

    """
    ACCESS_TYPES = ('create', 'update', 'read', 'delete', )

    source = serializers.CharField(required=True)
    target = serializers.CharField(required=True)
    access_type = serializers.ChoiceField(choices=ACCESS_TYPES)

    def check_perm(self, instance, access_type):
        """

        :param instance: Authorization instance
        :param access_type: permission type
        :return: True/False
        """
        return getattr(instance, access_type, False)
