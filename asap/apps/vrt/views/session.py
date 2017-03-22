#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.reverse import reverse_lazy

from asap.apps.vrt.models.session import Session
from asap.apps.vrt.serializers.session import SessionSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import DRFNestedViewMixin, AuthorableModelViewSet


class SessionViewSet(AuthorableModelViewSet, DRFNestedViewMixin,
                     viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_uuid', 'runtime__uuid')
    ]

    def create(self, request, *args, **kwargs):
        self.filter_nested_queryset(**kwargs)
        if self.is_nested:
            # we don't need to ask for the runtime to which the
            # session will be associated when the url is nested
            request.data.update(runtime=reverse_lazy('runtime-detail', kwargs={
                'uuid': kwargs.get('runtime_uuid')
            }))
        return super(SessionViewSet, self).create(request, *args, **kwargs)
