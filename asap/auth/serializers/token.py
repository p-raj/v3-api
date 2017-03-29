from rest_framework import serializers


# noinspection PyAbstractClass
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
