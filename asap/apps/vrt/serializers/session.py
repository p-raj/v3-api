from asap.apps.vrt.models.session import Session
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class SessionSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(lookup_field='uuid', view_name='runtimesession-detail')
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Session
        exclude = ('expires_at', 'uuid', 'author')

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'runtime': {
                'lookup_field': 'uuid'
            }
        }
