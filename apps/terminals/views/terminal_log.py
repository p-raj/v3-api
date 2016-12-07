from rest_framework import viewsets
from veris.router import Router

from ..serializers.terminal_log import TerminalLog, TerminalLogSerializer


class TerminalLogViewSet(viewsets.ModelViewSet):
    queryset = TerminalLog.objects.all()
    serializer_class = TerminalLogSerializer


router = Router()
router.register('terminal-logs', TerminalLogViewSet)
