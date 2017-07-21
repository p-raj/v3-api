from asap.apps.runtime.models.session import Session
from asap.utils.serializers import TimestampableModelSerializer

from rest_framework import serializers


class SessionSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(lookup_field='uuid', view_name='runtimesession-detail')

    class Meta:
        model = Session
        exclude = ('uuid', 'author',)
        read_only_fields = ('state',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'runtime': {
                'lookup_field': 'uuid'
            }
        }
