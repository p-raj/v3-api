from asap.apps.vrt.models.runtime_locker import RuntimeLocker
from asap.apps.vrt.serializers.runtime_locker import RuntimeLockerSerializer
from asap.router import Router

from rest_framework import viewsets


class RuntimeLockerViewSet(viewsets.ModelViewSet):
    queryset = RuntimeLocker.objects.all()
    serializer_class = RuntimeLockerSerializer

    lookup_field = 'uuid'


router = Router()
router.register('runtime-lockers', RuntimeLockerViewSet)
