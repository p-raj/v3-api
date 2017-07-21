from rest_framework.validators import UniqueTogetherValidator

from asap.apps.runtime.models.feedback import Feedback
from asap.utils.serializers import TimestampableModelSerializer

from rest_framework import serializers


class FeedbackSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Feedback
        fields = '__all__'

        extra_kwargs = {
            'app': {
                'lookup_field': 'uuid'
            }
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Feedback.objects.all(),
                fields=('author', 'app')
            )
        ]
