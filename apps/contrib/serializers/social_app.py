from rest_framework.reverse import reverse

from allauth.socialaccount.models import SocialApp
from rest_framework import serializers


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
