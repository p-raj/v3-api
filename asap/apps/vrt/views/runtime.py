#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets

from asap.apps.vrt.models.runtime import Runtime
from asap.apps.vrt.serializers.runtime import RuntimeSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


class RuntimeViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_locker_uuid', 'runtimelocker__uuid')
    ]
