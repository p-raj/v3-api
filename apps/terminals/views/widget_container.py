from rest_framework import viewsets

from ..serializers.widget_container import WidgetContainer, WidgetContainerSerializer


class WidgetContainerViewSet(viewsets.ModelViewSet):
    queryset = WidgetContainer.objects.all()
    serializer_class = WidgetContainerSerializer
