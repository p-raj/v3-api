#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.widgets.models.widget_locker import WidgetLocker
from asap.apps.widgets.serializers.widget_locker import WidgetLockerSerializer
from asap.core.views import AuthorableModelViewSet
from asap.router import Router

from rest_framework import viewsets


class WidgetLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = WidgetLocker.objects.all()
    serializer_class = WidgetLockerSerializer

    lookup_field = 'uuid'


router = Router()
router.register('widget-lockers', WidgetLockerViewSet)
