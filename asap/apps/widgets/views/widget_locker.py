#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.views.widget_locker
~~~~~~~~~~~~~~

- This file contains the Widget Locker service views, Every incoming http from runtime to get list of widgets
    will come here.

 """

# future
from __future__ import unicode_literals

# DRF
from rest_framework import viewsets, permissions

# local
from asap.core.views import AuthorableModelViewSet

# own app
from asap.apps.widgets.models.widget_locker import WidgetLocker
from asap.apps.widgets.serializers.widget_locker import WidgetLockerSerializer


class WidgetLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    """Widget Locker Viewset , will be used to fetch widgets in locker their schema, rules etc.

    """
    queryset = WidgetLocker.objects.all()
    serializer_class = WidgetLockerSerializer
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny,)

    lookup_field = 'token'
