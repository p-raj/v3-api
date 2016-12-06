from rest_framework import viewsets
from veris.router import Router

from ..serializers.organizations import Organization, OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def perform_create(self, serializer):
        # let's assume the we have a middleware that keeps us
        # in sync with the remote server's authentication
        # ``request.user`` is always authentic
        serializer.save(user_id=self.request.user.id)


router = Router()
router.register('organizations', OrganizationViewSet)
