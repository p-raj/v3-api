import requests
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend

from asap.core.signals.policy import AM_SERVER_HEADER, AM_SERVER_URL


class AMFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        The author should only be able to see only his objects.
        :return:
        """
        response = requests.get(
            url='{server}/micro-service/am/policy/list/?source={source}'.format(**{
                'server': AM_SERVER_URL,
                'source': request.user.username
            }),
            headers=AM_SERVER_HEADER
        )

        permissions = response.json().get('source_permission_set', [])
        return queryset.filter(
            Q(is_published=True) |
            Q(uuid__in=[
                _.get('target').split(':')[-2]
                for _ in permissions
                if _.get('read')
            ])
        )
