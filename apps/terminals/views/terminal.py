from rest_framework import viewsets

from ..serializers.terminal import Terminal, TerminalSerializer


class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
