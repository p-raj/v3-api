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


class DRFNestedViewMixin(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    Nested View support using drf-nested-routers.
    """
    # (lookup, query)
    lookup_parent = [
    ]

    @property
    def is_nested(self):
        # boolean to change the behavior of the API endpoint if required
        # for example
        # `/org/1/members/` should return the members of org 1 (available only on management portal or admins)
        # `/members/` should return the memberships of the user
        # itself across all organizations (available elsewhere)
        _nested = getattr(self, '_nested', None)
        assert _nested is not None, '`is_nested` accessed before `filter_nested_queryset`'
        return _nested

    def make_queryset(self):
        """
        A hook to further change the queryset depending
        on the called endpoint.

        for example:
        `/org/1/members/` should return the members of org 1 (available only on management portal or admins)
        `/members/` should return the memberships of the user
        itself across all organizations (available elsewhere)
        """
        return self.get_queryset()

    def filter_nested_queryset(self, **kwargs):
        queryset_filters = Q()

        setattr(self, '_nested', False)
        for lookup, query in self.lookup_parent:
            if not kwargs.get(lookup):
                # lookup field was not provided
                # probably a direct access to the endpoint
                # or an access via a different parent
                # let the defaults apply (if any)
                continue

            setattr(self, '_nested', True)
            queryset_filters &= Q(**{
                query: kwargs.get(lookup, None)
            })

        self.queryset = self.make_queryset().filter(queryset_filters)

    def list(self, request, *args, **kwargs):
        self.filter_nested_queryset(**kwargs)
        # lets not re-invent the wheel, follow DRY approach and let drf
        # handle the response once the queryset has been filtered
        return super(DRFNestedViewMixin, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.filter_nested_queryset(**kwargs)
        # lets not re-invent the wheel, follow DRY approach and let drf
        # handle the response once the queryset has been filtered
        return super(DRFNestedViewMixin, self).retrieve(request, *args, **kwargs)
