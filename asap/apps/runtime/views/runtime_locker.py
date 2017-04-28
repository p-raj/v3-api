#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import response, status, viewsets
from rest_framework.decorators import detail_route

from asap.apps.runtime.models.runtime_locker import RuntimeLocker
from asap.apps.runtime.serializers.runtime import RuntimeSerializer
from asap.apps.runtime.serializers.runtime_locker import RuntimeLockerSerializer
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

    @detail_route(methods=['POST'], lookup_field='uuid')
    def add(self, request, **kwargs):
        # expect either an existing runtime
        # object/url or a new instance
        # FIXME
        # not perfect yet, but works :/
        runtime_serializer = RuntimeSerializer(data=request.data, context=self.get_serializer_context())
        runtime_serializer.is_valid(raise_exception=True)
        runtime = runtime_serializer.save(author=request.user)

        runtime_locker = self.get_object()
        runtime_locker.runtimes.add(runtime)
        return self.retrieve(request, None, **kwargs)
