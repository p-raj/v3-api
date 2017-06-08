from asap.apps.runtime.models.feedback import Feedback
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class FeedbackSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        exclude = ('author', )

        extra_kwargs = {
            'app': {
                'lookup_field': 'uuid'
            }
        }
