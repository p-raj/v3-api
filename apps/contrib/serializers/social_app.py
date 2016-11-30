from allauth.socialaccount.models import SocialApp
from rest_framework import serializers


class SocialAppSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialApp
        fields = ['id', 'url', 'provider', 'client_id']

        extra_kwargs = {
            'url': {
                'lookup_field': 'provider'
            }
        }
