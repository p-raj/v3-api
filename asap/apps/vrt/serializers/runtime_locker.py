from rest_framework import serializers

from asap.apps.vrt.models.runtime import Runtime
from asap.apps.vrt.models.runtime_locker import RuntimeLocker
from asap.apps.vrt.serializers.runtime import RuntimeSerializer
from asap.core.serializers import TimestampableModelSerializer
from asap.fields.hyperlinked_serialized_related_field import HyperlinkedSerializedRelatedField


class RuntimeLockerSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    runtimes = HyperlinkedSerializedRelatedField(
        view_name='runtime-detail', many=True,
        serializer=RuntimeSerializer,
        queryset=Runtime.objects.all(),
        style={
            'base_template': 'input.html'
        },
        lookup_field='uuid'
    )

    class Meta:
        model = RuntimeLocker
        exclude = ('author',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'runtimes': {
                'lookup_field': 'uuid'
            }
        }
