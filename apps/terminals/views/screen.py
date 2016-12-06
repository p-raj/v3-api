from rest_framework import viewsets
from veris.router import Router

from ..serializers.screen import Screen, ScreenSerializer


class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


router = Router()
router.register('screens', ScreenViewSet)
