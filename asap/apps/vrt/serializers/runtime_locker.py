from asap.apps.vrt.models.runtime_locker import RuntimeLocker
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class RuntimeLockerSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuntimeLocker
        exclude = ('runtimes', 'author')

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'runtimes': {
                'lookup_field': 'uuid'
            }
        }
