from rest_framework import viewsets

from ..serializers import (Revision, RevisionSerializer)


class RevisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for ``Revision`` model.
    """
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer
