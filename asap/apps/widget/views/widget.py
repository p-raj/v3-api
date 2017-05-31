#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from asap.apps.widget.models.widget import Widget
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_uuid', 'widgetlocker__uuid')
    ]

    def get_queryset(self):
        queryset = super(WidgetViewSet, self).get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
