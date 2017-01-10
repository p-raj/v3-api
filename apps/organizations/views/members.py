from rest_framework import response, status, viewsets

from veris.router import Router
from ..serializers.members import Member, MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def list(self, request, *args, **kwargs):
        if not kwargs.get('organization_pk'):
            # let's disable the direct access of this url :)
            # saves a lot of permission checking etc etc
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        self.queryset = self.queryset.filter(organization=kwargs.get('organization_pk'))
        return super(MemberViewSet, self).list(request, *args, **kwargs)


# we have created the nested routes as well
router = Router()
router.register('members', MemberViewSet)
