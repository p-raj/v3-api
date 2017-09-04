import logging
from urllib.parse import urlencode
from wsgiref.util import is_hop_by_hop

import requests
from django.utils.functional import cached_property
from rest_framework import response, views
from rest_framework.permissions import AllowAny

from asap.apps.process.models import Process

logger = logging.getLogger(__name__)


class ProcessExecution(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if request.content_type != 'application/json':
            resp = requests.request(
                self.link.action,
                self.outgoing_url,
                data=request.data,
                files=request.FILES,
                headers=self.outgoing_headers()
            )
        else:
            resp = requests.request(
                self.link.action,
                self.outgoing_url,
                json=self.outgoing_data(),
                params=self.outgoing_params(),
                headers=self.outgoing_headers()
            )

        headers = {}
        for key, value in resp.headers.items():
            if is_hop_by_hop(key):
                continue

            if key.lower() in ['content-length']:
                continue

            headers[key] = value

        data = resp.json() \
            if resp.headers['Content-Type'].startswith('application/json') \
            else resp.content

        return response.Response(
            data=data,
            status=resp.status_code,
            headers=headers
        )

    def outgoing_params(self):
        params = {}
        for field in self.link.fields:
            if field.location == 'query':
                value = self.request.data.get(field.name)
                if value is None:
                    continue
                params[field.name] = value
        return urlencode(params)

    def outgoing_data(self):
        data = {}
        for field in self.link.fields:
            if field.location == 'form':
                value = self.request.data.get(field.name)
                if value is None:
                    continue
                data[field.name] = value
        return data

    def outgoing_headers(self):
        headers = {'Host': self.client.url}
        for field in self.link.fields:
            if field.location == 'header':
                value = self.request.data.get(field.name)
                if value is None:
                    continue
                headers[field.name] = value
        return headers

    @cached_property
    def outgoing_url(self):
        return self.link.url.format(**self.request.data)

    @cached_property
    def process(self):
        return Process.objects.get(uuid=self.kwargs.get('uuid'))

    @cached_property
    def client(self):
        return self.process.schema_client

    @cached_property
    def link(self):
        return self.client.get('api')
