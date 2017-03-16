#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- - micro_services.state_machine.serializers
~~~~~~~~~~~~~~

- **file description**
"""

# future
from __future__ import unicode_literals

# 3rd party
from datetime import datetime
from rest_framework import serializers


# Django


# local


# own app
from asap.micro_services.state_machine import config
from asap.micro_services.state_machine.models import TransactionLifeCycle, TransactionStateMachine, HttpService


class TransactionStateMachineSerializer(serializers.ModelSerializer):
    """

    """
    state = serializers.ChoiceField(required=True,
                                    choices=config.STATES)

    class Meta:
        model = TransactionStateMachine
        exclude = ('created_at', 'modified_at', )

    def create(self, validated_data):
        """

        :param validated_data: validated data
        :return:
        """
        created_at = modified_at = datetime.now()

        validated_data.update({
            'created_at': created_at,
            'modified_at': modified_at
        })

        return super(TransactionStateMachineSerializer, self).create(validated_data)


class TransactionLifeCycleSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = TransactionLifeCycle
        fields = '__all__'


class HttpServiceSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = HttpService
        fields = '__all__'


