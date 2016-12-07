from allauth.socialaccount.models import SocialApp

from django.contrib.sites.models import Site

from rest_framework import serializers, viewsets
from rest_framework.reverse import reverse

from veris.router import Router


class SocialAppSerializer(serializers.HyperlinkedModelSerializer):
    callback_url = serializers.SerializerMethodField()

    class Meta:
        model = SocialApp
        fields = ['id', 'url', 'provider', 'client_id',
                  'callback_url']

        extra_kwargs = {
            'url': {
                'lookup_field': 'provider'
            }
        }

    def get_callback_url(self, obj):
        return reverse('api_{provider}_login'.format(**{
            'provider': obj.provider
        }), request=self.context.get('request'))


class SocialAppViewSet(viewsets.ModelViewSet):
    queryset = SocialApp.objects.all()
    serializer_class = SocialAppSerializer

    lookup_field = 'provider'

    def get_queryset(self):
        queryset = super(SocialAppViewSet, self).get_queryset()
        site = Site.objects.get_current(self.request)
        return queryset.filter(sites=site)


router = Router()
router.register('social-apps', SocialAppViewSet)
