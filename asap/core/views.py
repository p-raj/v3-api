"""
ViewSetMixins for the project.
"""

from django.db.models import Q

from rest_framework import (mixins, viewsets)


class AuthorableModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSetMixin for models inheriting the abstract ``Authorable`` model.
    """

    def perform_create(self, serializer):
        """
        override: save the author from the request

        :param serializer:
        :return:
        """
        serializer.save(author=self.request.user)


class DRFNestedViewMixin(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Nested View support using drf-nested-routers.
    """
    # (lookup, query)
    lookup_parent = [
    ]

    def nest_queryset(self, **kwargs):
        queryset_filters = Q()

        for lookup, query in self.lookup_parent:
            queryset_filters &= Q(**{
                query: kwargs.get(lookup, None)
            })

        # lets not re-invent the wheel, follow DRY approach and let drf
        # handle the response once the queryset has been filtered
        self.queryset = self.get_queryset().filter(queryset_filters)

    def list(self, request, *args, **kwargs):
        self.nest_queryset(**kwargs)
        return super(DRFNestedViewMixin, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.nest_queryset(**kwargs)
        return super(DRFNestedViewMixin, self).retrieve(request, *args, **kwargs)
