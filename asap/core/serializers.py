from django.conf import settings
from rest_framework import serializers

DATETIME_FORMAT = getattr(settings, 'DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S%z')


class AuthorableModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer Mixin for models using Authorable Mixins.
    """
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        """
        :param obj:
        :return:
        """
        from asap.apps.authentication.views.users import UserSerializer

        user_serializer = UserSerializer(obj.author, context=self.context)
        return user_serializer.data


class TimestampableModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer Mixin for models using Timestampable Mixins.
    """
    # strip off milli seconds,
    # some clients don't handle this properly :/
    created_at = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT)
    modified_at = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT)
