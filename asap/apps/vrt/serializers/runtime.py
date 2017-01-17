from asap.apps.vrt.models.runtime import Runtime

from rest_framework import serializers


class RuntimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Runtime
        exclude = ('user',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
