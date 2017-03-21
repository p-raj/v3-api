#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.core.serializers import AuthorableModelSerializer
from asap.apps.organizations.models.organizations import Organization


class OrganizationSerializer(AuthorableModelSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Organization
        exclude = ()
