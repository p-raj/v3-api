from rest_framework import viewsets

from ..serializers.screen import Screen, ScreenSerializer


class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer
