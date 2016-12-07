from django.contrib.auth import get_user_model
from django.http.response import Http404

from rest_framework import serializers, viewsets
from veris.router import Router

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username']

        extra_kwargs = {
            'url': {
                'lookup_field': 'username'
            }
        }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Http404:
            serializer = self.get_serializer(data=kwargs)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return super(UserViewSet, self).retrieve(request, *args, **kwargs)


router = Router()
router.register('users', UserViewSet)
