from asap.apps.runtime.models.runtime import Runtime
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class RuntimeSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    has_feedback = serializers.ReadOnlyField()

    class Meta:
        model = Runtime
        exclude = ('author', 'is_published', 'widgets')

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
