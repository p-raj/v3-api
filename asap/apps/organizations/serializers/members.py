from rest_framework import serializers

from ..models.members import Member


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'url',
                  'organization',
                  'user']

        extra_kwargs = {
            'user': {
                'lookup_field': 'username'
            }
        }
