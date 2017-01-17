from rest_framework import serializers

from asap.core.serializers import AuthorableModelSerializer
from ..models.organizations import Organization


class OrganizationSerializer(AuthorableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        exclude = ()
