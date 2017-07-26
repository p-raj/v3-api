import logging

from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from rest_framework import renderers, response, status, views
from rest_framework.permissions import AllowAny

from asap.apps.process.models import Process

logger = logging.getLogger(__name__)


class ProcessExecution(views.APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [renderers.CoreJSONRenderer]

    def post(self, request, *args, **kwargs):
        try:
            client = self.process.client

            # default content-type is coreapi+json
            data = client.execute(params=request.data, **kwargs)

            # FIXME
            meta = getattr(data, 'title', '200 OK') or '200 OK'
            meta = meta if type(meta) == str else '200 OK'
            return response.Response(
                data,
                status=int(meta.split()[0]),
                content_type=request.content_type
            )
        except ValidationError as e:
            return response.Response({
                'errors': e.message.args
            },
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )

    @cached_property
    def process(self):
        return Process.objects.get(uuid=self.kwargs.get('uuid'))
