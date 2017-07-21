import reversion
from rest_framework import viewsets, response
from rest_framework.decorators import detail_route
from reversion.models import Version

from asap.utils.serializers import VersionSerializer


class VersionableModelViewSet(viewsets.GenericViewSet):
    """
    ViewSetMixin for models that have been registered with ``django-reversion``.
    """

    @detail_route()
    def history(self, request, **kwargs):
        """
        gets the history of a particular instance

        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object()
        versions = Version.objects.get_for_object(obj)

        version_serializer = VersionSerializer(
            versions,
            many=True,
            context={
                'request': request
            }
        )
        return response.Response(version_serializer.data)


class VersionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List all the versions of all the objects in the database.
    """
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    @detail_route()
    def revert(self, request, *args, **kwargs):
        """
        revert to the version specified

        :param request:
        :param pk:
        :return:
        """
        self.get_object().revert()
        return self.retrieve(request, *args, **kwargs)
