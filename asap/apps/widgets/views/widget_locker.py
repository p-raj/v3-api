#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets

from asap.apps.widgets.models.widget_locker import WidgetLocker
from asap.apps.widgets.serializers.widget_locker import WidgetLockerSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet


class WidgetLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = WidgetLocker.objects.all()
    serializer_class = WidgetLockerSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    lookup_field = 'token'
