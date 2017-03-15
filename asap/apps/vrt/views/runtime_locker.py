#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import response, status, viewsets
from rest_framework.decorators import detail_route

from asap.apps.vrt.models.runtime_locker import RuntimeLocker
from asap.apps.vrt.serializers.runtime_locker import RuntimeLockerSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet


class RuntimeLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = RuntimeLocker.objects.all()
    serializer_class = RuntimeLockerSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    lookup_field = 'uuid'

    @detail_route(methods=['POST'])
    def session(self, request, pk=None):
        # TODO
        # now, we need a runtime type
        # session timeout for terminal type runtimes

        # return a list of widgets to be shown next
        # if the session has already been initialized
        # let's get back here after starting widgets
        # lots of ambiguous doubts :/
        # can't even start
        return response.Response(status=status.HTTP_200_OK)
