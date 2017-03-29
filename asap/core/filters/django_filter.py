import operator

from django.db import models

from functools import reduce

from rest_framework.filters import BaseFilterBackend


class DjangoFilter(BaseFilterBackend):
    """
    Enable lookups on all fields on all relations.
    """

    def filter_queryset(self, request, queryset, view):
        """
        assume all query_params are correct and
        handle cases as they arrive

        :param request:
        :param queryset:
        :param view:
        :return:
        """
        lookup_fields = getattr(view, 'lookup_fields', None)
        if not lookup_fields:
            # there is no field to look up
            # get out and leave the queryset alone
            return queryset

        # filter out the query params
        # which are allowed for lookups
        lookups = [key for field in lookup_fields
                   for key, value in request.query_params.items()
                   if key.startswith(field)]

        if not lookups:
            # there is no field to look up
            # get out and leave the queryset alone
            return queryset

        and_queries = [models.Q(**{lookup_field: value})
                       for lookup_field, value in request.query_params.items()
                       if lookup_field in lookups]
        queryset = queryset.filter(reduce(operator.and_, and_queries)).distinct()
        return queryset
