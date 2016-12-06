from rest_framework import viewsets
from veris.router import Router

from ..serializers.members import Member, MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


router = Router()
router.register('members', MemberViewSet)
