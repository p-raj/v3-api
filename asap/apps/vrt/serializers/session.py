from asap.apps.vrt.models.session import Session
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class SessionSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Session
        exclude = ('expires_at', 'uuid',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'runtime': {
                'lookup_field': 'uuid'
            }
        }
