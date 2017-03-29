from rest_framework import serializers


# noinspection PyAbstractClass
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    # TODO create a password field to be used
    password = serializers.CharField()
