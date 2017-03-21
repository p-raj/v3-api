from rest_framework import serializers

from asap.apps.organizations.serializers.services import ServiceSerializer
from asap.core.serializers import AuthorableModelSerializer
from asap.fields.hyperlinked_serialized_related_field import HyperlinkedSerializedRelatedField
from ..models.organizations import Organization


class OrganizationSerializer(AuthorableModelSerializer, serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    services = HyperlinkedSerializedRelatedField(
        source='service_set', view_name='service-list',
        serializer=ServiceSerializer, many=True, read_only=True
    )

    class Meta:
        model = Organization
        exclude = ()
