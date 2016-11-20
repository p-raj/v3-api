import json
import requests

from rest_framework import serializers


class RemoteUserField(serializers.CharField):
    """
    RemoteUserField get the reference id of the ``User`` as stored on the remote server.
    It makes the assumption that the remote server will register the user
    silently and return a reference to the resource.
    """

    def to_internal_value(self, data):
        # let's make another assumption, the remote server
        # is hosted on the same machine :)
        response = requests.get('http://localhost:8000/api/v1/users/{}/'.format(data))
        user = json.loads(response.content.decode())
        return super(RemoteUserField, self).to_internal_value(user.get('id'))
