from asap.apps.vrt.models.runtime import Runtime
from asap.apps.vrt.serializers.runtime import RuntimeSerializer
from asap.core.views import DRFNestedViewMixin
from asap.router import Router

from rest_framework import viewsets


class RuntimeViewSet(DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_locker_uuid', 'runtimelocker__uuid')
    ]

    def perform_create(self, serializer):
        # let's assume the we have a middleware that ensures
        # only authenticated & authorized users reach here
        serializer.save(user_id=self.request.user.id)


router = Router()
router.register('runtimes', RuntimeViewSet)
