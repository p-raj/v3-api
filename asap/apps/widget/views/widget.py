#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from rest_framework import viewsets

from asap.apps.widget.models.widget import Widget
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.core.filters.am_filter import AMFilter
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    filter_backends = (AMFilter,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_uuid', 'widgetlocker__uuid')
    ]
