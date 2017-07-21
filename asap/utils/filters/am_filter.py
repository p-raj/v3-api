import requests

from django.conf import settings
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class AMFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        The author should only be able to see only his objects.
        :return:
        """
        response = requests.get(
            url='{server}/micro-service/am/policy/list/?source={source}'.format(**{
                'server': getattr(settings, 'V3__API_GATEWAY'),
                'source': request.user.username
            }),
            headers={
                'Host': getattr(settings, 'V3__HOST_AUTHORIZATION')
            })

        permissions = response.json().get('source_permission_set', [])
        return queryset.filter(
            Q(is_published=True) |
            Q(uuid__in=[
                _.get('target').split(':')[-2]
                for _ in permissions
                if _.get('read')
            ])
        )
