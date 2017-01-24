from asap.apps.process.models import Process
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class ProcessSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        exclude = ()

        extra_kwargs = {
            'url': {
                'lookup_field': 'token'
            }
        }
