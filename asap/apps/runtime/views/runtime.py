#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.runtime.serializers.runtime import RuntimeSerializer
from asap.core.filters.am_filter import AMFilter
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


class RuntimeViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer
    filter_backends = (AMFilter,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_locker_uuid', 'runtimelocker__uuid')
    ]
