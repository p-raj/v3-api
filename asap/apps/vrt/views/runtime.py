from rest_framework import viewsets, permissions

from asap.apps.vrt.models.runtime import Runtime
from asap.apps.vrt.serializers.runtime import RuntimeSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from asap.router import Router


class RuntimeViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    """

    """
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_locker_uuid', 'runtimelocker__uuid')
    ]

    def make_queryset(self):
        queryset = super(RuntimeViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # TODO
        # return all the runtimes
        # available to the requesting user
        return queryset


router = Router()
router.register('runtimes', RuntimeViewSet)
