from rest_framework import viewsets

from asap.core.views import AuthorableModelViewSet
from asap.router import Router
from ..serializers.organizations import Organization, OrganizationSerializer


class OrganizationViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def filter_queryset(self, queryset):
        return self.queryset.authored_by(self.request.user)


router = Router()
router.register('organizations', OrganizationViewSet)
