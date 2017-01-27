from rest_framework import viewsets
from rest_framework.reverse import reverse_lazy

from asap.apps.vrt.models.session import Session
from asap.apps.vrt.serializers.session import SessionSerializer
from asap.core.views import DRFNestedViewMixin


class SessionViewSet(DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_uuid', 'runtime__uuid')
    ]

    def make_queryset(self):
        queryset = super(SessionViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # TODO
        # return all the sessions
        # available after a&a
        return queryset

    def create(self, request, *args, **kwargs):
        self.filter_nested_queryset(**kwargs)
        if self.is_nested:
            # we don't need to ask for the runtime to which the
            # session will be associated when the url is nested
            request.data.update(runtime=reverse_lazy('runtime-detail', kwargs={
                'uuid': kwargs.get('runtime_uuid')
            }))
        return super(SessionViewSet, self).create(request, *args, **kwargs)
