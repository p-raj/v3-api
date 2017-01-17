from asap.apps.vrt.models.runtime import Runtime
from asap.apps.vrt.serializers.runtime import RuntimeSerializer
from asap.router import Router

from rest_framework import viewsets


class RuntimeViewSet(viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer

    lookup_field = 'uuid'

    def perform_create(self, serializer):
        # let's assume the we have a middleware that ensures
        # only authenticated & authorized users reach here
        serializer.save(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        if not kwargs.get('runtime_locker_uuid'):
            # let's assume if the runtime locker pk is missing
            # the user wants to access all of hte runtimes created by him
            self.queryset = self.queryset.filter(user=request.user)
            return super(RuntimeViewSet, self).list(request, *args, **kwargs)

        self.queryset = self.queryset.filter(runtimelocker__uuid=kwargs.get('runtime_locker_uuid'))
        return super(RuntimeViewSet, self).list(request, *args, **kwargs)


router = Router()
router.register('runtimes', RuntimeViewSet)
