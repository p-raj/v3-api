from asap.apps.vrt.models.runtime_locker import RuntimeLocker

from rest_framework import serializers


class RuntimeLockerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuntimeLocker
        exclude = ('runtimes',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'runtimes': {
                'lookup_field': 'uuid'
            }
        }
