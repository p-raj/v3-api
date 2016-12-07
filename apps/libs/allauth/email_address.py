from allauth.account.models import EmailAddress

from django.utils.translation import ugettext_lazy as _

from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from veris.router import Router


class EmailAddressSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the ``EmailAddress`` model
    """
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = EmailAddress
        fields = ['id', 'url', 'user', 'email', 'verified', 'primary']
        read_only_fields = ('verified', 'primary')

        extra_kwargs = {
            'user': {
                'lookup_field': 'username'
            }
        }


class EmailAddressViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    ViewSet for ``EmailAddress`` model.
    """
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Send a confirmation mail, once the email has been added.

        :param serializer:
        :return:
        """
        email_address = serializer.save(user=self.request.user)
        email_address.send_confirmation(self.request)

    def destroy(self, request, *args, **kwargs):
        """
        User should not be able to remove the **primary** email address.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        obj = self.get_object()
        resp = {
            'errors': [
                _('can not remove primary email address.')
            ]
        }
        if obj.primary:
            return Response(resp, status=status.HTTP_412_PRECONDITION_FAILED)

        return super(EmailAddressViewSet, self).destroy(request, *args, **kwargs)

    @detail_route()
    def resend_confirmation(self, request, pk=None):
        """
        Resend the confirmation email on this email address..

        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object()
        if obj.verified:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        obj.send_confirmation(request)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @detail_route()
    def make_primary(self, request, pk=None):
        """
        Mark the current email address as primary.

        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object()
        if obj.primary:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        obj.set_as_primary()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


router = Router()
router.register('email-addresses', EmailAddressViewSet)
