from rest_framework import serializers

from asap.apps.authentication.views.users import UserSerializer
from asap.apps.organizations.serializers.organizations import OrganizationSerializer
from asap.fields.hyperlinked_serialized_related_field import HyperlinkedSerializedRelatedField
from ..models.members import Member


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    user = HyperlinkedSerializedRelatedField(
        read_only=True,
        view_name='user-detail',
        serializer=UserSerializer
    )
    organization = HyperlinkedSerializedRelatedField(
        read_only=True,
        view_name='organization-detail',
        serializer=OrganizationSerializer
    )

    class Meta:
        model = Member
        exclude = ('author',)

        extra_kwargs = {
            'user': {
                'lookup_field': 'username'
            }
        }
