#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from rest_framework import viewsets

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.runtime.serializers.runtime import RuntimeSerializer
from asap.core.filters.am_filter import AMFilter
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class RuntimeViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer
    filter_backends = (AMFilter,)

    lookup_field = 'uuid'
