#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.process.models import ProcessLocker
from asap.apps.process.serializers.process_locker import ProcessLockerSerializer
from asap.core.filters.author_filter import AuthorFilter
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet

from rest_framework import viewsets


class ProcessLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = ProcessLocker.objects.all()
    serializer_class = ProcessLockerSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (AuthorFilter,)

    lookup_field = 'uuid'
