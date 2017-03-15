#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.apps.organizations.models.services import Service


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    is_enabled = serializers.BooleanField()

    class Meta:
        model = Service
        exclude = ('author',)
