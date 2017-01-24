from asap.apps.process.models import ProcessLocker
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class ProcessLockerSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessLocker
        exclude = ()

        extra_kwargs = {
            'url': {
                'lookup_field': 'token'
            }
        }
