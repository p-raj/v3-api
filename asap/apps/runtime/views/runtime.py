#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.runtime.serializers.runtime import RuntimeSerializer
from asap.core.filters.am_filter import AMFilter
from asap.core.filters.django_filter import DjangoFilter
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class RuntimeViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer
    filter_backends = (
        AMFilter, DjangoFilter,
        OrderingFilter, SearchFilter
    )

    lookup_field = 'uuid'
    lookup_fields = (
        'name', 'description'
    )
    ordering_fields = (
        'created_at', 'modified_at'
    )

    def get_queryset(self):
        queryset = super(RuntimeViewSet, self).get_queryset()
        if self.request.user.is_authenticated():
            return queryset.annotate_has_feedback(self.request.user)
        return queryset
