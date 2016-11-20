from rest_framework import serializers
from veris.fields import RemoteUserField

from ..models.members import Member


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    # we'll see how to validate the contact later
    # the user contact will be sent to server
    # the server finds the user on the remote server
    # and stores it id here
    # TODO
    # let's play on username for now instead of contact,
    # we'll have to manage less table
    member = RemoteUserField(write_only=True)

    class Meta:
        model = Member
        fields = ['id', 'url',
                  'organization',
                  'member']

    def create(self, validated_data):
        # we placed a write only field that interacts with remote server
        validated_data['user_id'] = validated_data.pop('member')
        return super(MemberSerializer, self).create(validated_data)
