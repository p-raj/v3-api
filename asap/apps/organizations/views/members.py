from rest_framework import viewsets

from asap.core.views import DRFNestedViewMixin
from asap.router import Router
from ..serializers.members import Member, MemberSerializer


class MemberViewSet(DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    lookup_parent = [
        ('organization_pk', 'organization')
    ]


# we have created the nested routes as well
router = Router()
router.register('members', MemberViewSet)
