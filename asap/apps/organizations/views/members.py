from rest_framework import viewsets

from asap.core.views import DRFNestedViewMixin, AuthorableModelViewSet
from asap.router import Router
from ..serializers.members import Member, MemberSerializer


class MemberViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    lookup_parent = [
        ('organization_pk', 'organization')
    ]

    def make_queryset(self):
        queryset = super(MemberViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # return all the memberships
        # available to the requesting user
        return queryset.filter(user=self.request.user)


# we have created the nested routes as well
router = Router()
router.register('members', MemberViewSet)
