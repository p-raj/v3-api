from django.contrib.sites.models import Site

from rest_framework import viewsets

from ..serializers.social_app import SocialApp, SocialAppSerializer


class SocialAppViewSet(viewsets.ModelViewSet):
    queryset = SocialApp.objects.all()
    serializer_class = SocialAppSerializer

    lookup_field = 'provider'

    def get_queryset(self):
        queryset = super(SocialAppViewSet, self).get_queryset()
        site = Site.objects.get_current(self.request)
        return queryset.filter(sites=site)
