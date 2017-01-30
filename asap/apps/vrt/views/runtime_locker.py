from asap.apps.vrt.models.runtime_locker import RuntimeLocker
from asap.apps.vrt.serializers.runtime_locker import RuntimeLockerSerializer
from asap.core.views import AuthorableModelViewSet
from asap.router import Router

from rest_framework import viewsets, response, status
from rest_framework.decorators import detail_route


class RuntimeLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    """

    """
    queryset = RuntimeLocker.objects.all()
    serializer_class = RuntimeLockerSerializer

    lookup_field = 'uuid'

    @detail_route(methods=['POST'])
    def session(self, request, pk=None):
        # TODO
        # now, we need a runtime type
        # session timeout for terminal type runtimes

        # return a list of widgets to be shown next
        # if the session has already been initialized
        # let's get back here after starting widgets
        # lots of ambiguous doubts :/
        # can't even start
        return response.Response(status=status.HTTP_200_OK)


router = Router()
router.register('runtime-lockers', RuntimeLockerViewSet)
