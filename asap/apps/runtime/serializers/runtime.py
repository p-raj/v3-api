from asap.apps.runtime.models.runtime import Runtime
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class RuntimeSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Runtime
        exclude = ('author',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
