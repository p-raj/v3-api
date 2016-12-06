from rest_framework import viewsets
from veris.router import Router

from ..serializers.terminal import Terminal, TerminalSerializer


class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer


router = Router()
router.register('terminals', TerminalViewSet)
